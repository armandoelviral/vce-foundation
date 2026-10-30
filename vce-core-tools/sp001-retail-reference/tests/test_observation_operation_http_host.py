from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from test_retail_observation_operation import values
from sp001.contracts.retail_observation_operation import (
    RetailObservationOperationReceipt as Receipt,
    RetailObservationEffectDisposition as Disposition,
    RetailObservationOperationConflict,
)
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict,
)
from sp001.infrastructure.observation_operation_http_host import (
    create_observation_operation_app,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)
from sp001.infrastructure.sqlite_observation_operations import (
    ObservationOperationIntegrityFailure,
)


class Service:
    def __init__(self):
        request, identity, stored = values()
        self.request = request
        self.receipt = Receipt(identity, stored, Disposition.CREATED)
        self.error = None
        self.calls = []
        self.responses = None

    def save(self, **kwargs):
        raise AssertionError("legacy route not expected")

    def recover(self, **kwargs):
        raise AssertionError("legacy route not expected")

    def save_operation(self, **kwargs):
        self.calls.append(("save", kwargs))
        if self.error:
            raise self.error
        return self.receipt

    def recover_operation(self, **kwargs):
        self.calls.append(("recover", kwargs))
        if self.error:
            raise self.error
        if self.responses is not None:
            return self.responses.pop(0)
        return self.receipt


def environment():
    service = Service()
    client = TestClient(create_observation_operation_app(service=service))
    identity = service.receipt.operation
    route = (
        f"/v1/cases/{identity.case_id}/"
        f"inspection-observation-operations/{identity.request_id}"
    )
    return service, client, route


HEADERS = {"Authorization": "Bearer synthetic-token"}
JSON_HEADERS = {**HEADERS, "Content-Type": "application/json"}


def test_save_then_recovery_has_distinct_contracts():
    service, client, route = environment()
    document = service.receipt.stored_observation.document
    saved = client.put(route, content=document, headers=JSON_HEADERS)
    assert saved.status_code == 200
    assert saved.json()["status"] == "saved"
    assert "observation_document" not in saved.json()
    recovered = client.get(route, headers=HEADERS)
    assert recovered.status_code == 200
    assert recovered.json()["status"] == "ok"
    assert recovered.json()["observation_document"] == document
    assert recovered.json()["observation_version"] == str(
        service.request.observation.observation_version,
    )
    assert recovered.headers["cache-control"] == "no-store"


def test_authorized_absence():
    service, client, route = environment()
    service.receipt = None
    result = client.get(route, headers=HEADERS)
    assert result.status_code == 404
    assert result.json() == {"status": "operation_not_found"}


@pytest.mark.parametrize("method", ["get", "put"])
def test_missing_credential_never_calls_service(method):
    service, client, route = environment()
    result = getattr(client, method)(route)
    assert result.status_code == 401
    assert service.calls == []


@pytest.mark.parametrize("error,code,status", [
    (Rejected("secret"), 401, "credential_rejected"),
    (Denied("secret"), 403, "access_denied"),
    (RetailObservationOperationConflict("secret"), 409, "operation_conflict"),
    (RetailInspectionObservationConflict("secret"), 409, "observation_conflict"),
    (ObservationOperationIntegrityFailure("secret"), 503, "integrity_failure"),
    (OSError("secret"), 503, "save_unconfirmed"),
])
def test_save_error_classification(error, code, status):
    service, client, route = environment()
    service.error = error
    result = client.put(
        route, content=service.receipt.stored_observation.document,
        headers=JSON_HEADERS,
    )
    assert result.status_code == code
    assert result.json()["status"] == status
    assert "secret" not in result.text
    assert "observation_document" not in result.json()
    if code in (401, 403, 503):
        assert result.json()["save_outcome"] == "unconfirmed"


@pytest.mark.parametrize("error,code,status", [
    (Rejected("secret"), 401, "credential_rejected"),
    (Denied("secret"), 403, "access_denied"),
    (ObservationOperationIntegrityFailure("secret"), 503, "integrity_failure"),
    (OSError("secret"), 503, "backend_unavailable"),
])
def test_recovery_error_classification(error, code, status):
    service, client, route = environment()
    service.error = error
    result = client.get(route, headers=HEADERS)
    assert result.status_code == code
    assert result.json() == {"status": status}
    assert "secret" not in result.text


@pytest.mark.parametrize("final", ["absent", "changed", "revoked"])
def test_final_recovery_prevents_delivery_of_prepared_content(final):
    service, client, route = environment()
    original = service.receipt
    if final == "revoked":
        def recover(**kwargs):
            if service.calls:
                raise Denied("secret")
            service.calls.append(("recover", kwargs))
            return original
        service.recover_operation = recover
    else:
        changed = replace(original, disposition=Disposition.REUSED)
        service.responses = [
            original, None if final == "absent" else changed,
        ]
    result = client.get(route, headers=HEADERS)
    assert result.status_code == (403 if final == "revoked" else 503)
    assert "observation_document" not in result.json()


def test_invalid_document_never_calls_service():
    service, client, route = environment()
    result = client.put(route, content="{}", headers=JSON_HEADERS)
    assert result.status_code == 400
    assert service.calls == []


def test_body_limit_never_calls_service():
    service, _, route = environment()
    client = TestClient(create_observation_operation_app(
        service=service, max_request_bytes=1,
    ))
    result = client.put(route, content="{}", headers=JSON_HEADERS)
    assert result.status_code == 413
    assert service.calls == []
