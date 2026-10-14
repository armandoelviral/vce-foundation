from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation, CaseAccessPermission,
)
from sp001.contracts.case_access_issuance_request import CaseAccessIssuanceRequest


def request():
    return CaseAccessIssuanceRequest(
        "REQUEST-1", "CASE-001", CaseAccessOperation.READ_STATE,
    )


def test_request_contains_only_caller_intent():
    assert tuple(field.name for field in fields(request())) == (
        "request_id", "case_id", "operation",
    )
    assert request().permission == CaseAccessPermission(
        "CASE-001", CaseAccessOperation.READ_STATE,
    )


@pytest.mark.parametrize("operation", list(CaseAccessOperation))
def test_nominal_operations_can_be_requested(operation):
    value = CaseAccessIssuanceRequest("REQUEST-1", "CASE-001", operation)
    assert value.permission.operation is operation


@pytest.mark.parametrize("value", ["", " ", "REQUEST 1", "R\n1", "R\x001"])
def test_invalid_request_identifier(value):
    with pytest.raises(ValueError):
        CaseAccessIssuanceRequest(value, "CASE-001", CaseAccessOperation.READ_STATE)


@pytest.mark.parametrize("value", [None, 1, True])
def test_request_identifier_requires_string(value):
    with pytest.raises(TypeError):
        CaseAccessIssuanceRequest(value, "CASE-001", CaseAccessOperation.READ_STATE)


@pytest.mark.parametrize("value", ["READ_STATE", None, 1])
def test_operation_requires_nominal_enum(value):
    with pytest.raises(TypeError):
        CaseAccessIssuanceRequest("REQUEST-1", "CASE-001", value)


def test_security_fields_cannot_be_supplied():
    with pytest.raises(TypeError):
        CaseAccessIssuanceRequest(
            request_id="REQUEST-1", case_id="CASE-001",
            operation=CaseAccessOperation.READ_STATE, subject="chosen-subject",
        )


def test_request_is_immutable():
    value = request()
    with pytest.raises(FrozenInstanceError):
        value.case_id = "OTHER"
    assert not hasattr(value, "__dict__")
