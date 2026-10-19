from dataclasses import replace

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission as Permission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.services.retail_report_access_policy import (
    required_retail_report_permissions,
    token_allows_retail_report,
)


def access(*operations):
    return ValidatedCaseAccessContext(
        principal=AuthenticatedPrincipal("ISSUER-TEST", "SUBJECT-TEST"),
        audience="REPORTS-TEST",
        issued_at=100, not_before=110, expires_at=200,
        permissions=tuple(Permission("CASE-1", op) for op in operations),
    )


def allows(context, **overrides):
    args = dict(
        access=context, case_id="CASE-1",
        expected_audience="REPORTS-TEST", at_time=150,
        recover_only=False,
    )
    args.update(overrides)
    return token_allows_retail_report(**args)


def test_save_requires_write_and_read_for_exact_case():
    assert required_retail_report_permissions(
        case_id="CASE-1", recover_only=False
    ) == (
        Permission("CASE-1", Operation.SAVE_RETAIL_REPORT),
        Permission("CASE-1", Operation.READ_RETAIL_REPORT),
    )


def test_recovery_requires_read_only():
    assert required_retail_report_permissions(
        case_id="CASE-1", recover_only=True
    ) == (Permission("CASE-1", Operation.READ_RETAIL_REPORT),)


@pytest.mark.parametrize("operations", [
    (), (Operation.READ_STATE,), (Operation.READ_LIFECYCLE_RESULT,),
    (Operation.SAVE_RETAIL_REPORT,), (Operation.READ_RETAIL_REPORT,),
])
def test_insufficient_permissions_do_not_allow_save(operations):
    assert not allows(access(*operations))


def test_save_and_recovery_with_explicit_permissions():
    context = access(Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT)
    assert allows(context)
    assert allows(context, recover_only=True)
    assert not allows(context, case_id="CASE-2")


def test_read_only_cannot_save():
    context = access(Operation.READ_RETAIL_REPORT)
    assert allows(context, recover_only=True)
    assert not allows(context)


@pytest.mark.parametrize("instant,expected", [
    (109, False), (110, True), (199, True), (200, False), (201, False),
])
def test_validity_boundaries(instant, expected):
    context = access(Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT)
    assert allows(context, at_time=instant) is expected


def test_rejects_wrong_audience_and_other_principal_gets_no_implicit_rights():
    context = access(Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT)
    assert not allows(context, expected_audience="OTHER")
    without_permissions = replace(
        context,
        principal=AuthenticatedPrincipal("OTHER-ISSUER", "OTHER-SUBJECT"),
        permissions=(),
    )
    assert not allows(without_permissions)


@pytest.mark.parametrize("value", [True, 1.5, "150", None])
def test_rejects_invalid_time_type(value):
    with pytest.raises(TypeError):
        allows(access(), at_time=value)


def test_rejects_negative_time():
    with pytest.raises(ValueError):
        allows(access(), at_time=-1)


@pytest.mark.parametrize("value", [0, 1, None])
def test_rejects_non_boolean_mode(value):
    with pytest.raises(TypeError):
        required_retail_report_permissions(
            case_id="CASE-1", recover_only=value
        )


def test_rejects_empty_case():
    with pytest.raises(ValueError):
        required_retail_report_permissions(
            case_id=" ", recover_only=True
        )
