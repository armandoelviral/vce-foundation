import sqlite3
import time
from dataclasses import replace

import pytest

import test_authenticated_inspection_observations_jwt as setup
from test_authenticated_observation_operations_jwt import (
    environment, credential, request,
)
from test_retail_report_jwt_composition import keys  # pytest fixture
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
)
from sp001.infrastructure.sqlite_observation_operations import (
    ObservationOperationIntegrityFailure,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def prepared(tmp_path, keys):
    service, _, _ = environment(tmp_path, keys)
    token = credential(keys, (setup.SAVE, setup.READ))
    item = request()
    receipt = service.save_operation(credential=token, request=item)
    return service, token, item, receipt


def invoke(service, token, item, operation):
    if operation == "save":
        return service.save_operation(credential=token, request=item)
    return service.recover_operation(
        credential=token,
        case_id=item.observation.case_id,
        request_id=item.request_id,
    )


def response(receipt, item, fault):
    if fault == "none":
        return None
    if fault == "mapping":
        return {"status": "committed"}
    if fault == "principal":
        return replace(receipt, operation=replace(
            receipt.operation,
            principal=AuthenticatedPrincipal("OTHER", "OTHER"),
        ))
    if fault == "request":
        return replace(receipt, operation=replace(
            receipt.operation, request_id="OTHER",
        ))
    if fault == "case":
        return replace(receipt, operation=replace(
            receipt.operation, case_id="OTHER",
        ))
    stored = receipt.stored_observation
    if fault == "key":
        stored = replace(stored, identity=replace(
            stored.identity, observation_id="OTHER",
        ))
    elif fault == "invalid_document":
        stored = replace(stored, document="{}")
    elif fault == "noncanonical":
        stored = replace(stored, document=stored.document + "\n")
    elif fault == "document_case":
        stored = replace(stored, document=serialize(replace(
            item.observation, case_id="OTHER",
        )))
    elif fault == "different_content":
        stored = replace(stored, document=serialize(replace(
            item.observation, description="Different backend content.",
        )))
    else:
        raise AssertionError("unknown test fault")
    return replace(receipt, stored_observation=stored)


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("fault", [
    "mapping", "principal", "request", "case",
    "key", "invalid_document", "noncanonical", "document_case",
])
def test_rejects_inconsistent_backend_response(
    tmp_path, keys, monkeypatch, operation, fault,
):
    service, token, item, receipt = prepared(tmp_path, keys)
    bad = response(receipt, item, fault)
    method = (
        "save_operation_authorized" if operation == "save"
        else "recover_operation_authorized"
    )
    monkeypatch.setattr(service._backend, method, lambda **kwargs: bad)
    with pytest.raises((TypeError, ValueError)):
        invoke(service, token, item, operation)


def test_save_rejects_different_valid_content(tmp_path, keys, monkeypatch):
    service, token, item, receipt = prepared(tmp_path, keys)
    bad = response(receipt, item, "different_content")
    monkeypatch.setattr(
        service._backend, "save_operation_authorized",
        lambda **kwargs: bad,
    )
    with pytest.raises(ValueError):
        service.save_operation(credential=token, request=item)


def test_none_is_allowed_only_as_recovery_absence(tmp_path, keys, monkeypatch):
    service, token, item, _ = prepared(tmp_path, keys)
    monkeypatch.setattr(
        service._backend, "recover_operation_authorized",
        lambda **kwargs: None,
    )
    assert invoke(service, token, item, "recover") is None
    monkeypatch.setattr(
        service._backend, "save_operation_authorized",
        lambda **kwargs: None,
    )
    with pytest.raises(TypeError):
        invoke(service, token, item, "save")


@pytest.mark.parametrize("operation", ["save", "recover"])
@pytest.mark.parametrize("error_type", [
    sqlite3.OperationalError,
    OSError,
    ObservationOperationIntegrityFailure,
])
def test_backend_failures_propagate_without_becoming_absence(
    tmp_path, keys, monkeypatch, operation, error_type,
):
    service, token, item, _ = prepared(tmp_path, keys)
    error = error_type("synthetic backend failure")

    def fail(**kwargs):
        raise error

    method = (
        "save_operation_authorized" if operation == "save"
        else "recover_operation_authorized"
    )
    monkeypatch.setattr(service._backend, method, fail)
    with pytest.raises(error_type) as caught:
        invoke(service, token, item, operation)
    assert caught.value is error


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_final_expiration_rejects_result_without_erasing_committed_pair(
    tmp_path, keys, monkeypatch, operation,
):
    service, token, item, receipt = prepared(tmp_path, keys)
    now = [int(time.time())]
    monkeypatch.setattr(service, "_clock", lambda: now[0])
    method = (
        "save_operation_authorized" if operation == "save"
        else "recover_operation_authorized"
    )
    original = getattr(service._backend, method)

    def expire_after_backend(**kwargs):
        result = original(**kwargs)
        now[0] += 10000
        return result

    with monkeypatch.context() as patch:
        patch.setattr(service._backend, method, expire_after_backend)
        with pytest.raises(Rejected):
            invoke(service, token, item, operation)

    now[0] = int(time.time())
    assert invoke(service, token, item, "recover") == receipt
