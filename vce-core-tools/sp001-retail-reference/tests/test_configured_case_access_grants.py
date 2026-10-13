from dataclasses import FrozenInstanceError, replace
import time

import pytest

from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.services.configured_case_access_grants import (
    ConfiguredCaseAccessGrants,
    GrantBackedCaseReadAuthorizer,
)


PRINCIPAL = AuthenticatedPrincipal("issuer-A", "subscriber-1")
PERMISSION = CaseAccessPermission("CASE-001", Operation.READ_STATE)


def grant():
    return CaseAccessGrant("GRANT-001", PRINCIPAL, PERMISSION, 100, 200)


@pytest.mark.parametrize("at_time,expected", [
    (99, False), (100, True), (199, True), (200, False),
])
def test_grant_validity_boundaries(at_time, expected):
    source = ConfiguredCaseAccessGrants(grants=(grant(),))
    assert source.permits(
        principal=PRINCIPAL, permission=PERMISSION, at_time=at_time
    ) is expected


@pytest.mark.parametrize("principal,permission", [
    (AuthenticatedPrincipal("issuer-B", "subscriber-1"), PERMISSION),
    (AuthenticatedPrincipal("issuer-A", "subscriber-2"), PERMISSION),
    (PRINCIPAL, CaseAccessPermission("OTHER", Operation.READ_STATE)),
    (PRINCIPAL, CaseAccessPermission("CASE-001", Operation.SUBSCRIBE_EVENTS)),
])
def test_identity_case_and_operation_are_exact(principal, permission):
    source = ConfiguredCaseAccessGrants(grants=(grant(),))
    assert not source.permits(
        principal=principal, permission=permission, at_time=150
    )


def test_empty_source_denies():
    assert not ConfiguredCaseAccessGrants(grants=()).permits(
        principal=PRINCIPAL, permission=PERMISSION, at_time=150
    )


def test_duplicate_grant_identifier_is_rejected():
    with pytest.raises(ValueError):
        ConfiguredCaseAccessGrants(grants=(grant(), grant()))


@pytest.mark.parametrize("field,value", [
    ("grant_id", ""), ("principal", None), ("permission", None),
    ("valid_from", True), ("expires_at", "200"), ("valid_from", -1),
    ("expires_at", 100),
])
def test_invalid_grant_is_rejected(field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(grant(), **{field: value})


def test_grant_is_immutable():
    with pytest.raises(FrozenInstanceError):
        grant().expires_at = 300


@pytest.mark.parametrize("token_permission,current_grant,expected", [
    (True, True, True), (True, False, False),
    (False, True, False), (False, False, False),
])
def test_authorizer_requires_token_permission_and_current_grant(
    token_permission, current_grant, expected,
):
    now = int(time.time())
    access = ValidatedCaseAccessContext(
        principal=PRINCIPAL, audience="coordinator",
        issued_at=now - 1, not_before=now - 1, expires_at=now + 100,
        permissions=(PERMISSION,) if token_permission else (),
    )
    current = CaseAccessGrant(
        "GRANT-001", PRINCIPAL, PERMISSION, now - 1, now + 100,
    )
    authorizer = GrantBackedCaseReadAuthorizer(
        grants=ConfiguredCaseAccessGrants(
            grants=(current,) if current_grant else (),
        )
    )
    assert authorizer.can_read_case(
        access=access, case_id="CASE-001"
    ) is expected


def test_expired_access_is_denied_even_with_current_grant():
    now = int(time.time())
    access = ValidatedCaseAccessContext(
        principal=PRINCIPAL, audience="coordinator",
        issued_at=now - 20, not_before=now - 20, expires_at=now - 1,
        permissions=(PERMISSION,),
    )
    source = ConfiguredCaseAccessGrants(grants=(
        CaseAccessGrant("GRANT-001", PRINCIPAL, PERMISSION, now - 20, now + 100),
    ))
    assert not GrantBackedCaseReadAuthorizer(grants=source).can_read_case(
        access=access, case_id="CASE-001"
    )
