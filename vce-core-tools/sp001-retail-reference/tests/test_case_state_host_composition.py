import asyncio
from dataclasses import replace
import socket
import threading
import time

import jwt
import pytest
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from test_case_state_https_loopback import certificates
from sp001.contracts.case_access_context import CaseAccessPermission, CaseAccessOperation
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord, GrantAdministrationAction as Action,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_state_read_result import NotFound
from sp001.infrastructure.case_state_host_composition import compose_case_state_host
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.services.case_access_grant_administration import administer_case_access_grant
from sp001.services.case_state_subscription import CaseStateSubscription
from sp001.services.case_state_reconciliation import ViewStatus


class Reader:
    def __init__(self):
        self.calls = []

    def read(self, *, case_id):
        self.calls.append(case_id)
        return NotFound(case_id)


@pytest.fixture
def key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def compose(reader, key, path, issuer="https://issuer.example"):
    return compose_case_state_host(
        reader=reader, issuer=issuer, audience="sp001-coordinator",
        public_keys={"key-1": key.public_key()},
        max_lifetime_seconds=300, max_token_bytes=8192,
        grants_database_path=path,
    )


def token(key):
    now = int(time.time())
    return jwt.encode(
        {
            "iss": "https://issuer.example", "sub": "subscriber-1",
            "aud": "sp001-coordinator",
            "iat": now - 1, "nbf": now - 1, "exp": now + 120,
            "case_permissions": [
                {"case_id": "CASE-001", "operation": "READ_STATE"},
            ],
        },
        key, algorithm="RS256", headers={"kid": "key-1", "typ": "at+jwt"},
    )


def test_empty_composed_store_grants_no_access(tmp_path, key):
    reader = Reader()
    app = compose(reader, key, tmp_path / "grants.sqlite3")
    with TestClient(app) as client:
        response = client.get(
            "/v1/cases/CASE-001/state",
            headers={"Authorization": "Bearer " + token(key)},
        )
    assert response.status_code == 403
    assert reader.calls == []
    assert SqliteCaseAccessGrants(
        database_path=tmp_path / "grants.sqlite3"
    ).read_audit() == ()


def test_invalid_verifier_config_creates_no_database(tmp_path, key):
    path = tmp_path / "grants.sqlite3"
    with pytest.raises(ValueError):
        compose(Reader(), key, path, issuer="")
    assert not path.exists()


def test_composed_host_observes_authorized_grant_and_revocation_over_https(tmp_path, key):
    path = tmp_path / "grants.sqlite3"
    reader = Reader()
    app = compose(reader, key, path)
    admin = AuthenticatedPrincipal("https://issuer.example", "administrator-1")
    principal = AuthenticatedPrincipal("https://issuer.example", "subscriber-1")
    now = int(time.time())
    granted = GrantAdministrationRecord(
        event_id="CREATE-1", actor=admin, action=Action.GRANT,
        grant=CaseAccessGrant(
            "GRANT-1", principal,
            CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE),
            now - 1, now + 300,
        ),
        recorded_at=now,
    )

    class Policy:
        def may_administer(self, *, actor, action, grant):
            return (
                actor == admin and grant == granted.grant
                and action in (Action.GRANT, Action.REVOKE)
            )

    writer = SqliteCaseAccessGrants(database_path=path)
    assert administer_case_access_grant(store=writer, policy=Policy(), record=granted)

    ca, certificate, tls_key = certificates(tmp_path)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(
        app, host="127.0.0.1", port=port,
        ssl_certfile=str(certificate), ssl_keyfile=str(tls_key),
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
                pytest.fail("composed host startup deadline exceeded")
            time.sleep(0.01)
        if failures:
            raise failures[0]
        assert server.started
        credential = token(key)
        subscription = CaseStateSubscription(
            reader=RemoteCaseStateReader(
                endpoint=f"https://localhost:{port}/v1/cases/{{caseId}}/state",
                timeout_seconds=2, max_response_bytes=4096, ca_file=str(ca),
                credential_provider=lambda: credential,
            ),
            case_id="CASE-001",
        )
        assert subscription.refresh().status is ViewStatus.NOT_FOUND
        assert reader.calls == ["CASE-001"]

        revoked = replace(
            granted, event_id="REVOKE-1", action=Action.REVOKE,
            recorded_at=int(time.time()),
        )
        assert administer_case_access_grant(
            store=writer, policy=Policy(), record=revoked,
        )
        assert time.time() < jwt.decode(
            credential, options={"verify_signature": False}
        )["exp"]
        view = subscription.refresh()
        assert view.status is ViewStatus.REQUEST_REJECTED
        assert view.reason.startswith("request_status:403:")
        assert reader.calls == ["CASE-001"]
        assert writer.read_audit() == (granted, revoked)
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        if thread.is_alive():
            pytest.fail("composed host shutdown deadline exceeded")
