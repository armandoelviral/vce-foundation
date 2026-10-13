from dataclasses import FrozenInstanceError, replace
import time

import pytest
from fastapi.testclient import TestClient

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    ValidatedCaseAccessContext, CaseAccessPermission, CaseAccessOperation,
)
from sp001.contracts.case_state_read_result import NotFound
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)


def context():
    now = int(time.time())
    return ValidatedCaseAccessContext(
        principal=AuthenticatedPrincipal("issuer-A", "subscriber-1"),
        audience="sp001-coordinator",
        issued_at=now - 10, not_before=now - 10, expires_at=now + 300,
        permissions=(CaseAccessPermission(
            "CASE-001", CaseAccessOperation.READ_STATE,
        ),),
    )


@pytest.mark.parametrize("field", ["issued_at", "not_before", "expires_at"])
@pytest.mark.parametrize("value", [True, "100", None, -1])
def test_invalid_timestamps_are_rejected(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(context(), **{field: value})


def test_invalid_interval_and_duplicate_permissions_are_rejected():
    access = context()
    with pytest.raises(ValueError):
        replace(access, expires_at=access.not_before)
    with pytest.raises(ValueError):
        replace(access, permissions=access.permissions * 2)


def test_context_is_immutable_and_contains_no_credential():
    access = context()
    with pytest.raises(FrozenInstanceError):
        access.audience = "other"
    assert not hasattr(access, "__dict__")
    assert not hasattr(access, "credential")


@pytest.mark.parametrize(
    "kind,status",
    [
        ("wrong_audience", 401),
        ("expired", 401),
        ("future", 401),
        ("wrong_case", 403),
        ("wrong_operation", 403),
        ("no_permissions", 403),
        ("valid", 404),
    ],
)
def test_host_checks_access_before_authorizer_and_reader(kind, status):
    access = context()
    now = int(time.time())
    if kind == "wrong_audience":
        access = replace(access, audience="sp001-sse")
    elif kind == "expired":
        access = replace(
            access, issued_at=now - 20, not_before=now - 20, expires_at=now - 1,
        )
    elif kind == "future":
        access = replace(
            access, issued_at=now + 10, not_before=now + 10, expires_at=now + 20,
        )
    elif kind == "wrong_case":
        access = replace(access, permissions=(
            CaseAccessPermission("OTHER", CaseAccessOperation.READ_STATE),
        ))
    elif kind == "wrong_operation":
        access = replace(access, permissions=(
            CaseAccessPermission("CASE-001", CaseAccessOperation.SUBSCRIBE_EVENTS),
        ))
    elif kind == "no_permissions":
        access = replace(access, permissions=())

    calls = []

    class Authenticator:
        def authenticate(self, *, credential):
            return access

    class Authorizer:
        def can_read_case(self, *, access, case_id):
            calls.append("authorize")
            return True

    class Reader:
        def read(self, *, case_id):
            calls.append("read")
            return NotFound(case_id)

    app = create_authenticated_case_state_app(
        reader=Reader(), authenticator=Authenticator(), authorizer=Authorizer(),
        expected_audience="sp001-coordinator",
    )
    with TestClient(app) as client:
        response = client.get(
            "/v1/case-state",
            params={"case_id": "CASE-001"},
            headers={"Authorization": "Bearer test-token"},
        )
    assert response.status_code == status
    assert calls == (["authorize", "read"] if kind == "valid" else [])
