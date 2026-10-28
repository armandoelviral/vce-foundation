from dataclasses import replace

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation,
    CaseAccessPermission as Permission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.services.retail_observation_access_policy import (
    required_retail_observation_permissions as required,
    token_allows_retail_observation,
)
from sp001.services.retail_report_access_policy import token_allows_retail_report


SAVE = Operation.SAVE_RETAIL_OBSERVATION
READ = Operation.READ_RETAIL_OBSERVATION


def context(*operations):
    return ValidatedCaseAccessContext(
        AuthenticatedPrincipal("ISSUER", "SUBJECT"),
        "OBSERVATIONS", 100, 110, 200,
        tuple(Permission("CASE", operation) for operation in operations),
    )


def allows(access, operation=SAVE, **overrides):
    arguments = dict(
        access=access, case_id="CASE", operation=operation,
        expected_audience="OBSERVATIONS", at_time=150,
    )
    arguments.update(overrides)
    return token_allows_retail_observation(**arguments)


@pytest.mark.parametrize("operation", [SAVE, READ])
def test_requires_only_the_exact_operation(operation):
    assert required(case_id="CASE", operation=operation) == (
        Permission("CASE", operation),
    )
    assert allows(context(operation), operation)


def test_save_and_read_are_independent():
    assert not allows(context(SAVE), READ)
    assert not allows(context(READ), SAVE)
    assert allows(context(SAVE, READ), SAVE)
    assert allows(context(SAVE, READ), READ)


@pytest.mark.parametrize("operation", list(Operation))
@pytest.mark.parametrize("requested", [SAVE, READ])
def test_each_permission_grants_only_its_exact_observation_operation(
    operation, requested,
):
    assert allows(context(operation), requested) is (operation is requested)


@pytest.mark.parametrize("requested", [SAVE, READ])
def test_combined_report_permissions_do_not_authorize_observations(requested):
    access = context(
        Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
    )
    assert not allows(access, requested)


@pytest.mark.parametrize("recover_only", [False, True])
def test_observation_permissions_do_not_authorize_reports(recover_only):
    assert not token_allows_retail_report(
        access=context(SAVE, READ), case_id="CASE",
        expected_audience="OBSERVATIONS", at_time=150,
        recover_only=recover_only,
    )


@pytest.mark.parametrize("operation", [SAVE, READ])
def test_no_permissions_and_wrong_case_are_denied(operation):
    assert not allows(context(), operation)
    assert not allows(context(operation), operation, case_id="OTHER")


@pytest.mark.parametrize("instant,expected", [
    (99, False), (109, False), (110, True),
    (199, True), (200, False), (201, False),
])
@pytest.mark.parametrize("operation", [SAVE, READ])
def test_validity_boundaries(instant, expected, operation):
    assert allows(context(operation), operation, at_time=instant) is expected


def test_wrong_audience_is_denied():
    assert not allows(context(SAVE), expected_audience="OTHER")


def test_declared_principal_does_not_supply_missing_permissions():
    access = replace(
        context(), principal=AuthenticatedPrincipal("OTHER", "OTHER"),
    )
    assert not allows(access)


@pytest.mark.parametrize("operation", [
    item for item in Operation if item not in (SAVE, READ)
])
def test_rejects_unrelated_requested_operation(operation):
    with pytest.raises(ValueError):
        required(case_id="CASE", operation=operation)


@pytest.mark.parametrize("operation", ["SAVE_RETAIL_OBSERVATION", None, True])
def test_rejects_untyped_operation(operation):
    with pytest.raises(TypeError):
        required(case_id="CASE", operation=operation)


@pytest.mark.parametrize("case_id,error", [
    ("", ValueError), (" ", ValueError), (None, TypeError),
])
def test_rejects_invalid_case(case_id, error):
    with pytest.raises(error):
        required(case_id=case_id, operation=READ)


@pytest.mark.parametrize("field,value,error", [
    ("access", None, TypeError),
    ("expected_audience", None, TypeError),
    ("expected_audience", " ", ValueError),
    ("at_time", True, TypeError),
    ("at_time", 1.5, TypeError),
    ("at_time", "150", TypeError),
    ("at_time", -1, ValueError),
])
def test_rejects_invalid_policy_inputs(field, value, error):
    with pytest.raises(error):
        allows(context(SAVE), **{field: value})
