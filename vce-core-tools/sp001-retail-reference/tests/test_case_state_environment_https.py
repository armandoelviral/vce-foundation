import asyncio
from dataclasses import replace
import json
import socket
import threading
import time

import jwt
import pytest
import uvicorn
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from test_case_state_https_loopback import certificates
from sp001.contracts.case_access_context import CaseAccessOperation, CaseAccessPermission
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord, GrantAdministrationAction as Action,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_state_read_result import RequestRejected
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.services.case_access_grant_administration import administer_case_access_grant
from sp001.services.case_state_reconciliation import ViewStatus
from sp001.services.case_state_subscription import CaseStateSubscription
from sp001.services.case_lifecycle_application import open_case
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def test_environment_factory_https_read_and_revocation(tmp_path, monkeypatch):
    signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_pem = signing_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    keys_path = tmp_path / "public-keys.json"
    keys_path.write_text(json.dumps({"key-1": public_pem}))
    case_path = tmp_path / "cases.sqlite3"
    grants_path = tmp_path / "grants.sqlite3"

    environment = {
        "SP001_AUTH_ISSUER": "https://issuer.example",
        "SP001_AUTH_AUDIENCE": "sp001-coordinator",
        "SP001_AUTH_PUBLIC_KEYS_FILE": str(keys_path),
        "SP001_AUTH_MAX_LIFETIME_SECONDS": "300",
        "SP001_AUTH_MAX_TOKEN_BYTES": "8192",
        "SP001_CASE_DATABASE_PATH": str(case_path),
        "SP001_GRANTS_DATABASE_PATH": str(grants_path),
    }
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    case_store = SqliteCaseAuthoritativeStateStore(database_path=case_path)
    expected = open_case(
        store=case_store, case_id="CASE-001", objective_id="OBJ-001",
        scope="STORE-001", transition_id="TRANSITION-1",
    )
    assert expected is not None

    now = int(time.time())
    admin = AuthenticatedPrincipal("https://issuer.example", "administrator-1")
    principal = AuthenticatedPrincipal("https://issuer.example", "subscriber-1")
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

    grants = SqliteCaseAccessGrants(database_path=grants_path)
    assert administer_case_access_grant(
        store=grants, policy=Policy(), record=granted,
    )
    credential = jwt.encode(
        {
            "iss": principal.issuer, "sub": principal.subject,
            "aud": "sp001-coordinator",
            "iat": now - 1, "nbf": now - 1, "exp": now + 120,
            "case_permissions": [
                {"case_id": "CASE-001", "operation": "READ_STATE"},
                {"case_id": "UNGRANTED", "operation": "READ_STATE"},
            ],
        },
        signing_key, algorithm="RS256",
        headers={"kid": "key-1", "typ": "at+jwt"},
    )

    ca, certificate, tls_key = certificates(tmp_path)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(
        "sp001.infrastructure.case_state_host_bootstrap:create_app",
        factory=True,
        host="127.0.0.1", port=port,
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
                pytest.fail("environment host startup deadline exceeded")
            time.sleep(0.01)
        if failures:
            raise failures[0]
        assert server.started

        def remote(provider=None):
            return RemoteCaseStateReader(
                endpoint=f"https://localhost:{port}/v1/case-state",
                timeout_seconds=2, max_response_bytes=4096,
                ca_file=str(ca), credential_provider=provider,
            )

        missing = remote().read(case_id="CASE-001")
        assert isinstance(missing, RequestRejected)
        assert missing.status_code == 401

        provider_calls = []

        def provider():
            provider_calls.append("credential")
            return credential

        secured_reader = remote(provider)
        denied = secured_reader.read(case_id="UNGRANTED")
        assert isinstance(denied, RequestRejected)
        assert denied.status_code == 403

        subscription = CaseStateSubscription(
            reader=secured_reader, case_id="CASE-001"
        )
        first = subscription.refresh()
        assert first.status is ViewStatus.CURRENT
        assert first.last_valid_state == expected

        revoked = replace(
            granted, event_id="REVOKE-1", action=Action.REVOKE,
            recorded_at=int(time.time()),
        )
        assert administer_case_access_grant(
            store=SqliteCaseAccessGrants(database_path=grants_path),
            policy=Policy(), record=revoked,
        )
        assert time.time() < now + 120
        second = subscription.refresh()
        assert second.status is ViewStatus.REQUEST_REJECTED
        assert second.reason.startswith("request_status:403:")
        assert second.last_valid_state is first.last_valid_state
        assert provider_calls == ["credential"] * 3
        assert grants.read_audit() == (granted, revoked)
        assert case_store.read(case_id="CASE-001") == expected
        assert len(case_store.read_transitions(case_id="CASE-001")) == 1
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        if thread.is_alive():
            pytest.fail("environment host shutdown deadline exceeded")
