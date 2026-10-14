import json
import ssl
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from test_case_state_https_loopback import certificates
from test_federated_case_access_issuance_integration import flow
from sp001.infrastructure import jwks_access_token_keys as module
from sp001.infrastructure.jwt_case_access_authenticator import AccessTokenKeyResolutionError
from sp001.infrastructure.jwt_federated_issuance_authenticator import (
    JwtFederatedIssuanceAuthenticator,
)


def public_jwk(key, kid):
    value = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    value.update(kid=kid, alg="RS256", use="sig")
    return value


@pytest.fixture
def jwks_host(tmp_path):
    ca, certificate, tls_key = certificates(tmp_path)
    signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    state = {
        "keys": [public_jwk(signing_key, "PRIMARY-1")],
        "status": 200,
        "requests": [],
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            state["requests"].append({
                "path": self.path,
                "authorization": self.headers.get("Authorization"),
            })
            body = json.dumps({"keys": state["keys"]}).encode()
            self.send_response(state["status"])
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls.load_cert_chain(str(certificate), str(tls_key))
    server.socket = tls.wrap_socket(server.socket, server_side=True)
    failures = []

    def run():
        try:
            server.serve_forever(poll_interval=0.01)
        except BaseException as error:
            failures.append(error)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        yield server.server_address[1], ca, signing_key, state
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive()
        assert failures == []


def resolver(host, *, trusted=True, hostname="localhost"):
    port, ca, _, _ = host
    return module.JwksAccessTokenKeys(
        issuer="external", jwks_url=f"https://{hostname}:{port}/jwks",
        cache_ttl_seconds=60, min_refresh_interval_seconds=10,
        timeout_seconds=2, max_response_bytes=8192, max_keys=10,
        ca_file=str(ca) if trusted else None,
    )


def authenticator(keys):
    return JwtFederatedIssuanceAuthenticator(
        issuer="external", audience="issuance-service",
        key_resolver=keys, max_lifetime_seconds=300, max_token_bytes=8192,
    )


def primary(key, kid="PRIMARY-1"):
    now = int(time.time())
    return jwt.encode(
        {
            "iss": "external", "sub": "external-subject",
            "aud": "issuance-service",
            "iat": now - 1, "nbf": now - 1, "exp": now + 180,
        },
        key, algorithm="RS256", headers={"kid": kid, "typ": "at+jwt"},
    )


def cache_clock(monkeypatch):
    clock = [0.0]
    # Replace only this module's time reference, not the global time module.
    monkeypatch.setattr(
        module, "time", SimpleNamespace(monotonic=lambda: clock[0]),
    )
    return clock


def test_real_https_jwks_authenticates_and_reuses_cache(jwks_host):
    _, _, key, state = jwks_host
    auth = authenticator(resolver(jwks_host))
    credential = primary(key)
    first = auth.authenticate(credential=credential)
    assert first.principal.subject == "external-subject"
    assert auth.authenticate(credential=credential) == first
    assert state["requests"] == [{"path": "/jwks", "authorization": None}]


@pytest.mark.parametrize("failure", ["untrusted_ca", "wrong_hostname"])
def test_tls_failure_is_provider_failure_before_http(jwks_host, failure):
    _, _, key, state = jwks_host
    keys = resolver(
        jwks_host, trusted=failure != "untrusted_ca",
        hostname="127.0.0.1" if failure == "wrong_hostname" else "localhost",
    )
    with pytest.raises(AccessTokenKeyResolutionError) as caught:
        authenticator(keys).authenticate(credential=primary(key))
    assert isinstance(caught.value.__cause__, ssl.SSLCertVerificationError)
    assert state["requests"] == []


def test_rotation_refreshes_and_retires_old_key(jwks_host, monkeypatch):
    clock = cache_clock(monkeypatch)
    _, _, old_key, state = jwks_host
    auth = authenticator(resolver(jwks_host))
    assert auth.authenticate(credential=primary(old_key)) is not None
    new_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    state["keys"] = [public_jwk(new_key, "PRIMARY-2")]
    new_token = primary(new_key, "PRIMARY-2")

    # Unknown kid cannot force refresh before the configured interval.
    assert auth.authenticate(credential=new_token) is None
    assert len(state["requests"]) == 1
    clock[0] = 10.0
    assert auth.authenticate(credential=new_token) is not None
    assert len(state["requests"]) == 2
    assert auth.authenticate(credential=primary(old_key)) is None
    assert len(state["requests"]) == 2


def test_expired_cache_and_503_do_not_accept_stale_key(jwks_host, monkeypatch):
    clock = cache_clock(monkeypatch)
    _, _, key, state = jwks_host
    auth = authenticator(resolver(jwks_host))
    credential = primary(key)
    assert auth.authenticate(credential=credential) is not None
    clock[0] = 60.0
    state["status"] = 503
    with pytest.raises(AccessTokenKeyResolutionError):
        auth.authenticate(credential=credential)
    # Subsequent attempt is bounded without another HTTP request.
    with pytest.raises(AccessTokenKeyResolutionError):
        auth.authenticate(credential=credential)
    assert len(state["requests"]) == 2


def test_unknown_key_is_token_rejection_with_successful_provider(jwks_host):
    _, _, key, state = jwks_host
    assert authenticator(resolver(jwks_host)).authenticate(
        credential=primary(key, "UNKNOWN"),
    ) is None
    assert len(state["requests"]) == 1


def test_https_jwks_reaches_preparation_completion_and_recovery(
    jwks_host, flow, monkeypatch,
):
    store, service, preparation, _, _, access_key = flow
    _, _, primary_key, state = jwks_host
    # Replace the local-key authenticator in the existing issuance test fixture.
    monkeypatch.setattr(
        service, "_authenticator", authenticator(resolver(jwks_host)),
    )
    credential = primary(primary_key)
    service.prepare(credential=credential, preparation=preparation)
    token = service.complete(
        credential=credential, request_id=preparation.request_id,
    )
    decoded = jwt.decode(
        token.credential, access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    )
    assert decoded == preparation.payload.to_claims()
    assert store.read_completed(request_id=preparation.request_id) is not None
    assert service.complete(
        credential=credential, request_id=preparation.request_id,
    ) == token
    assert state["requests"] == [{"path": "/jwks", "authorization": None}]
