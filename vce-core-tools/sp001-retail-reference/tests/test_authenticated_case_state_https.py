from dataclasses import replace
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord, GrantAdministrationAction,
)
from sp001.services.case_access_grant_administration import (
    administer_case_access_grant,
)

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    CaseAccessOperation, CaseAccessPermission,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.services.configured_case_access_grants import (
    ConfiguredCaseAccessGrants, GrantBackedCaseReadAuthorizer,
)

import asyncio
import socket
import threading
import time

import jwt
import pytest
import uvicorn
from cryptography.hazmat.primitives.asymmetric import rsa

from test_case_state_https_loopback import certificates
from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_state_read_result import Found, NotFound, RequestRejected
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)
from sp001.infrastructure.jwt_case_access_authenticator import (
    JwtCaseAccessAuthenticator,
)
from sp001.infrastructure.remote_case_state_reader import RemoteCaseStateReader
from sp001.services.case_state_reconciliation import ViewStatus
from sp001.services.case_state_subscription import CaseStateSubscription


@pytest.fixture
def secured_host(tmp_path):
    ca, certificate, tls_key = certificates(tmp_path)
    signing_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    verifier = JwtCaseAccessAuthenticator(
        issuer="https://issuer.example", audience="sp001-coordinator",
        public_keys={"key-1": signing_key.public_key()},
        max_lifetime_seconds=300, max_token_bytes=8192,
    )
    events = []
    access_policy = {"allowed": True}
    state = CaseAuthoritativeState(
        case_id="CASE-001", objective_id="OBJ-001", scope="STORE-001",
        phase=CaseLifecyclePhase.CASE_OPENED, revision=8, resource_links=(),
    )

    class Authenticator:
        def authenticate(self, *, credential):
            events.append("authenticate")
            return verifier.authenticate(credential=credential)

    now = int(time.time())
    principal = AuthenticatedPrincipal(
        "https://issuer.example", "subscriber-1"
    )
    grant_path = tmp_path / "access-grants.sqlite3"
    configured_grants = SqliteCaseAccessGrants(database_path=grant_path)
    administrator = AuthenticatedPrincipal(
        "https://issuer.example", "administrator-1"
    )

    class AdministrationPolicy:
        def may_administer(self, *, actor, action, grant):
            return (
                actor == administrator
                and grant.principal == principal
                and grant.permission.case_id in ("CASE-001", "MISSING")
                and action in (GrantAdministrationAction.GRANT,
                               GrantAdministrationAction.REVOKE)
            )

    administration_policy = AdministrationPolicy()
    grant_records = {}
    for case_id in ("CASE-001", "MISSING"):
        record = GrantAdministrationRecord(
            event_id=f"CREATE-{case_id}",
            actor=administrator,
            action=GrantAdministrationAction.GRANT,
            grant=CaseAccessGrant(
                grant_id=f"GRANT-{case_id}",
                principal=principal,
                permission=CaseAccessPermission(
                    case_id, CaseAccessOperation.READ_STATE
                ),
                valid_from=now - 30,
                expires_at=now + 300,
            ),
            recorded_at=now,
        )
        assert administer_case_access_grant(
            store=configured_grants, policy=administration_policy, record=record
        )
        grant_records[case_id] = record

    def revoke(case_id):
        revoked = replace(
            grant_records[case_id],
            event_id=f"REVOKE-{case_id}",
            action=GrantAdministrationAction.REVOKE,
            recorded_at=int(time.time()),
        )
        # Separate adapter instance writes to the same persistent database.
        writer = SqliteCaseAccessGrants(database_path=grant_path)
        assert administer_case_access_grant(
            store=writer, policy=administration_policy, record=revoked
        )
        return writer.read_audit()

    access_policy["revoke"] = revoke

    class GrantSource:
        def permits(self, *, principal, permission, at_time):
            events.append("authorize")
            return access_policy["allowed"] and configured_grants.permits(
                principal=principal,
                permission=permission,
                at_time=at_time,
            )

    authorizer = GrantBackedCaseReadAuthorizer(grants=GrantSource())

    class Reader:
        def read(self, *, case_id):
            events.append("read")
            return Found(state) if case_id == state.case_id else NotFound(case_id)

    app = create_authenticated_case_state_app(
        reader=Reader(), authenticator=Authenticator(), authorizer=authorizer,
        expected_audience="sp001-coordinator",
    )
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

    def issue(*, case_id="CASE-001", expired=False):
        now = int(time.time())
        return jwt.encode(
            {
                "iss": "https://issuer.example",
                "sub": "subscriber-1",
                "aud": "sp001-coordinator",
                "iat": now - 20,
                "nbf": now - 20,
                "exp": now - 1 if expired else now + 120,
                "case_permissions": [
                    {"case_id": case_id, "operation": "READ_STATE"},
                ],
            },
            signing_key, algorithm="RS256",
            headers={"kid": "key-1", "typ": "at+jwt"},
        )

    def reader(provider=None):
        return RemoteCaseStateReader(
            endpoint=f"https://localhost:{port}/v1/case-state",
            timeout_seconds=2, max_response_bytes=4096,
            ca_file=str(ca), credential_provider=provider,
        )

    try:
        deadline = time.monotonic() + 5
        while not server.started and thread.is_alive():
            if time.monotonic() >= deadline:
                pytest.fail("secured HTTPS host startup deadline exceeded")
            time.sleep(0.01)
        if failures:
            raise failures[0]
        if not server.started:
            pytest.fail("secured HTTPS host did not start")
        yield reader, issue, events, access_policy
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        if thread.is_alive():
            pytest.fail("secured HTTPS host shutdown deadline exceeded")


def test_https_jwt_authorization_read_and_reconciliation(secured_host):
    reader, issue, events, policy = secured_host
    provider_calls = []

    def provider():
        provider_calls.append("credential")
        return issue()

    subscription = CaseStateSubscription(
        reader=reader(provider), case_id="CASE-001"
    )
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state.revision == 8
    assert events == ["authenticate", "authorize", "read"]
    assert provider_calls == ["credential"]


@pytest.mark.parametrize("kind,status", [
    ("missing", 401), ("invalid", 401), ("expired", 401),
    ("wrong_case", 403), ("policy_denied", 403),
])
def test_rejection_does_not_read_or_retry(secured_host, kind, status):
    reader, issue, events, policy = secured_host
    provider_calls = []
    token = issue()
    if kind == "invalid":
        token = "broken"
    elif kind == "expired":
        token = issue(expired=True)
    elif kind == "wrong_case":
        token = issue(case_id="OTHER")
    elif kind == "policy_denied":
        policy["allowed"] = False

    def provider():
        provider_calls.append("credential")
        return token

    result = reader(None if kind == "missing" else provider).read(
        case_id="CASE-001"
    )
    assert isinstance(result, RequestRejected)
    assert result.status_code == status
    assert "read" not in events
    expected_events = (
        [] if kind == "missing"
        else ["authenticate", "authorize"] if kind == "policy_denied"
        else ["authenticate"]
    )
    assert events == expected_events
    assert provider_calls == ([] if kind == "missing" else ["credential"])


def test_credential_is_reloaded_and_rejection_preserves_view(secured_host):
    reader, issue, events, policy = secured_host
    current = {"token": issue()}
    subscription = CaseStateSubscription(
        reader=reader(lambda: current["token"]), case_id="CASE-001"
    )
    original = subscription.refresh().last_valid_state
    current["token"] = "broken"
    view = subscription.refresh()
    assert view.status is ViewStatus.REQUEST_REJECTED
    assert view.last_valid_state is original
    assert view.reason.startswith("request_status:401:")
    assert events == ["authenticate", "authorize", "read", "authenticate"]


def test_authorized_missing_case_remains_business_absence(secured_host):
    reader, issue, events, policy = secured_host
    subscription = CaseStateSubscription(
        reader=reader(lambda: issue(case_id="MISSING")), case_id="MISSING"
    )
    assert subscription.refresh().status is ViewStatus.NOT_FOUND
    assert events == ["authenticate", "authorize", "read"]


@pytest.mark.parametrize("credential", ["", None, "token\r\nInjected: value"])
def test_invalid_provider_output_is_rejected_before_network(secured_host, credential):
    reader, issue, events, policy = secured_host
    with pytest.raises(ValueError, match="invalid bearer value"):
        reader(lambda: credential).read(case_id="CASE-001")
    assert events == []


def test_token_is_header_only_and_redirect_is_not_followed(monkeypatch):
    from sp001.infrastructure import remote_case_state_reader as module

    calls = []
    credential = "test-token"

    class Response:
        status = 302

    class Connection:
        def __init__(self, *args, **kwargs):
            pass

        def request(self, method, target, headers):
            calls.append((target, headers))

        def getresponse(self):
            return Response()

        def close(self):
            pass

    monkeypatch.setattr(module.http.client, "HTTPSConnection", Connection)
    reader = RemoteCaseStateReader(
        endpoint="https://coordinator.example/v1/case-state",
        timeout_seconds=1, max_response_bytes=4096,
        credential_provider=lambda: credential,
    )
    result = reader.read(case_id="CASE-001")
    assert result.reason == "unexpected_http_status"
    assert len(calls) == 1
    target, headers = calls[0]
    assert credential not in target
    assert headers["Authorization"] == "Bearer " + credential


def test_signed_permission_without_configured_grant_is_denied(secured_host):
    reader, issue, events, policy = secured_host
    result = reader(lambda: issue(case_id="UNGRANTED")).read(
        case_id="UNGRANTED"
    )
    assert isinstance(result, RequestRejected)
    assert result.status_code == 403
    assert events == ["authenticate", "authorize"]


def test_local_grant_denial_preserves_previously_reconciled_view(secured_host):
    reader, issue, events, policy = secured_host
    subscription = CaseStateSubscription(
        reader=reader(lambda: issue()), case_id="CASE-001"
    )
    original = subscription.refresh().last_valid_state
    assert original is not None

    policy["allowed"] = False
    view = subscription.refresh()
    assert view.status is ViewStatus.REQUEST_REJECTED
    assert view.last_valid_state is original
    assert view.reason.startswith("request_status:403:")
    assert events == [
        "authenticate", "authorize", "read",
        "authenticate", "authorize",
    ]


def test_same_live_token_is_denied_after_durable_revocation(secured_host):
    reader, issue, events, policy = secured_host
    credential = issue()
    provider_calls = []

    def provider():
        provider_calls.append("credential")
        return credential

    subscription = CaseStateSubscription(
        reader=reader(provider), case_id="CASE-001"
    )
    first = subscription.refresh()
    assert first.status is ViewStatus.CURRENT
    original = first.last_valid_state
    assert original is not None

    audit = policy["revoke"]("CASE-001")
    assert len(audit) == 3
    assert audit[-1].action is GrantAdministrationAction.REVOKE
    assert audit[-1].grant.grant_id == "GRANT-CASE-001"

    # Decode only to assert the test token has not expired.
    # Production authentication still verifies its signature normally.
    expires_at = jwt.decode(
        credential, options={"verify_signature": False}
    )["exp"]
    assert time.time() < expires_at

    second = subscription.refresh()
    assert second.status is ViewStatus.REQUEST_REJECTED
    assert second.reason.startswith("request_status:403:")
    assert second.last_valid_state is original
    assert provider_calls == ["credential", "credential"]
    assert events == [
        "authenticate", "authorize", "read",
        "authenticate", "authorize",
    ]
