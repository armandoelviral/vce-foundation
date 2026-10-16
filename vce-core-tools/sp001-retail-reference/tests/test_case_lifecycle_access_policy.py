from dataclasses import replace

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission as Permission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.services.case_lifecycle_access_policy import (
    required_case_lifecycle_permissions as required,
    token_allows_case_lifecycle as allows,
)


def access(permissions):
    return ValidatedCaseAccessContext(
        principal=AuthenticatedPrincipal("ISSUER", "OPERATOR"),
        audience="COORDINATOR",
        issued_at=100, not_before=100, expires_at=200,
        permissions=permissions,
    )


def check(context, request_value, recover_only=False, at_time=150):
    return allows(
        access=context, request=request_value,
        expected_audience="COORDINATOR",
        at_time=at_time, recover_only=recover_only,
    )


@pytest.mark.parametrize("factory,operation", [
    (opening, Operation.OPEN_CASE),
    (completion, Operation.APPLY_CASE_TRANSITION),
])
def test_execute_requires_operation_and_result_read(factory, operation):
    request_value = factory().request
    permissions = required(request=request_value, recover_only=False)
    assert permissions == (
        Permission("CASE-1", operation),
        Permission("CASE-1", Operation.READ_LIFECYCLE_RESULT),
    )
    assert check(access(permissions), request_value)
    for permission in permissions:
        assert not check(access((permission,)), request_value)


@pytest.mark.parametrize("factory", [opening, completion])
def test_recovery_needs_current_result_read_claim_without_write_claim(factory):
    request_value = factory().request
    permissions = required(request=request_value, recover_only=True)
    assert permissions == (
        Permission("CASE-1", Operation.READ_LIFECYCLE_RESULT),
    )
    assert check(access(permissions), request_value, recover_only=True)
    assert not check(access(permissions), request_value)


@pytest.mark.parametrize("operation", [
    Operation.READ_STATE, Operation.SUBSCRIBE_EVENTS,
])
def test_existing_read_permissions_do_not_authorize_lifecycle_result(operation):
    context = access((Permission("CASE-1", operation),))
    assert not check(context, opening().request)
    assert not check(context, opening().request, recover_only=True)


def test_permissions_for_another_case_are_not_accepted():
    permissions = (
        Permission("OTHER", Operation.OPEN_CASE),
        Permission("OTHER", Operation.READ_LIFECYCLE_RESULT),
    )
    assert not check(access(permissions), opening().request)


def test_transition_permission_does_not_authorize_opening():
    permissions = (
        Permission("CASE-1", Operation.APPLY_CASE_TRANSITION),
        Permission("CASE-1", Operation.READ_LIFECYCLE_RESULT),
    )
    assert not check(access(permissions), opening().request)


@pytest.mark.parametrize("at_time,expected", [
    (99, False), (100, True), (199, True), (200, False),
])
def test_validity_boundaries(at_time, expected):
    permissions = required(request=opening().request, recover_only=False)
    assert check(access(permissions), opening().request, at_time=at_time) is expected


def test_wrong_audience_is_rejected():
    permissions = required(request=opening().request, recover_only=False)
    assert not check(
        replace(access(permissions), audience="OTHER"),
        opening().request,
    )


@pytest.mark.parametrize("value", [None, object()])
def test_invalid_context_is_rejected(value):
    with pytest.raises(TypeError):
        check(value, opening().request)


def test_recovery_mode_does_not_accept_truthy_values():
    with pytest.raises(TypeError):
        required(request=opening().request, recover_only=1)
