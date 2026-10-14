import asyncio
from dataclasses import replace
import http.client
import json
import socket
import ssl
import threading
import time

import jwt
import pytest
import uvicorn

from test_case_access_issuer_composition import configuration
from test_case_state_https_loopback import certificates
from test_federated_case_access_issuance_integration import flow
from test_federated_jwks_https import jwks_host, resolver, primary
from sp001.contracts.case_access_grant_administration import GrantAdministrationAction
from sp001.infrastructure.case_access_issuer_host_composition import (
    compose_case_access_issuer_host,
)


@pytest.fixture
def issuer_https(configuration, jwks_host, flow, tmp_path):
    store, _, _, command, _, access_key = flow
    configuration.update(
        primary_key_resolver=resolver(jwks_host),
        signing_private_key=access_key,
        authorization_database_path=tmp_path / "authorization.sqlite3",
    )
    app = compose_case_access_issuer_host(
        max_request_bytes=1024, max_primary_credential_bytes=8192,
        **configuration,
    )
    directory = tmp_path / "issuer-tls"
    directory.mkdir()
    ca, certificate, key = certificates(directory)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(
        app, host="127.0.0.1", port=port,
        ssl_certfile=str(certificate), ssl_keyfile=str(key),
        lifespan="off", loop="asyncio", access_log=False,
        log_level="critical", timeout_graceful_shutdown=1,
    ))
    failures = []

    def run():
        try:
            asyncio.run(server.serve(sockets=[listener]))
        except BaseException as error:
            failures.append(error)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 5
        while not server.started and thread.is_alive():
            if time.monotonic() >= deadline:
                pytest.fail("issuer HTTPS startup deadline exceeded")
            time.sleep(0.01)
        assert failures == []
        assert server.started
        yield port, ca, store, command, access_key, jwks_host
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        assert not thread.is_alive()
        assert failures == []


def post(host, *, credential=None, case_id="CASE-001",
         trusted=True, hostname="localhost"):
    port, ca, _, _, _, _ = host
    context = ssl.create_default_context(cafile=str(ca) if trusted else None)
    connection = http.client.HTTPSConnection(
        hostname, port=port, timeout=3, context=context,
    )
    headers = {"Content-Type": "application/json"}
    if credential is not None:
        headers["Authorization"] = "Bearer " + credential
    try:
        connection.request(
            "POST", "/v1/case-access-token",
            body=json.dumps({
                "request_id": "HTTPS-REQUEST", "case_id": case_id,
                "operation": "READ_STATE",
            }),
            headers=headers,
        )
        response = connection.getresponse()
        body = response.read(16385)
        assert len(body) <= 16384
        return response.status, dict(response.getheaders()), json.loads(body)
    finally:
        connection.close()


def test_both_https_links_reach_durable_completion_and_recovery(issuer_https):
    _, _, store, _, access_key, jwks = issuer_https
    _, _, primary_key, state = jwks
    credential = primary(primary_key)
    status, headers, body = post(issuer_https, credential=credential)
    assert status == 200
    assert headers["cache-control"] == "no-store"
    prepared = store.read_prepared(request_id="HTTPS-REQUEST")
    completed = store.read_completed(request_id="HTTPS-REQUEST")
    assert completed is not None
    assert jwt.decode(
        body["access_token"], access_key.public_key(), algorithms=["RS256"],
        issuer="access", audience="coordinator",
    ) == prepared.payload.to_claims()
    replay_status, _, replay = post(issuer_https, credential=credential)
    assert replay_status == 200
    assert replay["access_token"] == body["access_token"]
    assert store.read_completed(request_id="HTTPS-REQUEST") == completed
    assert state["requests"] == [{"path": "/jwks", "authorization": None}]


def test_missing_primary_returns_401_without_jwks_or_preparation(issuer_https):
    _, _, store, _, _, jwks = issuer_https
    status, _, body = post(issuer_https)
    assert status == 401
    assert "access_token" not in body
    assert store.read_prepared(request_id="HTTPS-REQUEST") is None
    assert jwks[3]["requests"] == []


def test_case_without_grant_returns_403_without_preparation(issuer_https):
    _, _, store, _, _, jwks = issuer_https
    status, _, body = post(
        issuer_https, credential=primary(jwks[2]), case_id="OTHER",
    )
    assert status == 403
    assert "access_token" not in body
    assert store.read_prepared(request_id="HTTPS-REQUEST") is None


def test_revoked_grant_denies_https_recovery(issuer_https):
    _, _, store, command, _, jwks = issuer_https
    credential = primary(jwks[2])
    assert post(issuer_https, credential=credential)[0] == 200
    historical = store.read_completed(request_id="HTTPS-REQUEST")
    store.apply(record=replace(
        command, event_id="HTTPS-REVOKE", action=GrantAdministrationAction.REVOKE,
    ))
    status, _, body = post(issuer_https, credential=credential)
    assert status == 403
    assert "access_token" not in body
    assert store.read_completed(request_id="HTTPS-REQUEST") == historical


def test_failed_jwks_returns_503_without_preparation(issuer_https):
    _, _, store, _, _, jwks = issuer_https
    jwks[3]["status"] = 503
    status, _, body = post(issuer_https, credential=primary(jwks[2]))
    assert status == 503
    assert body["code"] == "KEY_PROVIDER_UNAVAILABLE"
    assert "access_token" not in body
    assert store.read_prepared(request_id="HTTPS-REQUEST") is None
    assert len(jwks[3]["requests"]) == 1


@pytest.mark.parametrize("failure", ["untrusted_ca", "wrong_hostname"])
def test_issuer_tls_failure_precedes_issuance(issuer_https, failure):
    _, _, store, _, _, jwks = issuer_https
    with pytest.raises(ssl.SSLCertVerificationError):
        post(
            issuer_https, credential=primary(jwks[2]),
            trusted=failure != "untrusted_ca",
            hostname="127.0.0.1" if failure == "wrong_hostname" else "localhost",
        )
    assert store.read_prepared(request_id="HTTPS-REQUEST") is None
    assert jwks[3]["requests"] == []
