from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from test_retail_inspection_observation import observation
import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys

from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
)
from sp001.infrastructure.inspection_observation_http_host import (
    create_inspection_observation_app as create_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)


ROUTE = "/v1/cases/CASE-1/inspection-observations/OBS-1/versions/1"
HEADERS = {
    "Authorization": "Bearer synthetic-token",
    "Content-Type": "application/json",
}


class Service:
    def __init__(self, error=None, changed=False):
        self.calls = []
        self.error = error
        self.changed = changed

    def recover(self, **kwargs):
        return None

    def save(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        item = kwargs["observation"]
        return replace(item, description="Different") if self.changed else item


def test_returns_receipt_without_document():
    service = Service()
    with TestClient(create_app(service=service)) as client:
        result = client.put(
            ROUTE, content=serialize(observation()), headers=HEADERS,
        )
    assert result.status_code == 200
    assert result.json() == {
        "status": "saved", "observation_id": "OBS-1",
        "observation_version": "1",
    }
    assert service.calls[0]["observation"] == observation()
    assert result.headers["cache-control"] == "no-store"
    assert "synthetic-token" not in result.text


@pytest.mark.parametrize("error,code,status,uncertain", [
    (Rejected("private"), 401, "credential_rejected", True),
    (Denied("private"), 403, "access_denied", True),
    (Conflict("private"), 409, "observation_conflict", False),
    (OSError("private"), 503, "save_unconfirmed", True),
])
def test_errors_preserve_uncertainty_without_content(
    error, code, status, uncertain,
):
    with TestClient(create_app(service=Service(error=error))) as client:
        result = client.put(
            ROUTE, content=serialize(observation()), headers=HEADERS,
        )
    expected = {"status": status}
    if uncertain:
        expected["save_outcome"] = "unconfirmed"
    assert result.status_code == code
    assert result.json() == expected
    assert "private" not in result.text
    assert "observation_document" not in result.json()


def test_inconsistent_confirmation_is_unconfirmed():
    with TestClient(create_app(service=Service(changed=True))) as client:
        result = client.put(
            ROUTE, content=serialize(observation()), headers=HEADERS,
        )
    assert result.status_code == 503
    assert result.json()["save_outcome"] == "unconfirmed"


@pytest.mark.parametrize("document", [
    "{}", "[]", "not json", serialize(observation()) + "\n",
    serialize(observation(case_id="OTHER")),
    serialize(observation(observation_version=2)),
    serialize(observation(observation_id="OTHER")),
])
def test_invalid_or_mismatched_document_never_calls_save(document):
    service = Service()
    with TestClient(create_app(service=service)) as client:
        result = client.put(ROUTE, content=document, headers=HEADERS)
    assert result.status_code == 400
    assert service.calls == []


def test_body_limit_applies_to_streamed_bytes():
    service = Service()
    with TestClient(create_app(
        service=service, max_request_bytes=10,
    )) as client:
        result = client.put(
            ROUTE, content=iter([b"123456", b"789012"]), headers=HEADERS,
        )
    assert result.status_code == 413
    assert service.calls == []


@pytest.mark.parametrize("headers,code", [
    ({"Content-Type": "application/json"}, 401),
    ({**HEADERS, "Authorization": "Basic token"}, 401),
    ({**HEADERS, "Content-Type": "text/plain"}, 415),
    ({**HEADERS, "Content-Encoding": "gzip"}, 415),
])
def test_invalid_request_headers_do_not_call_save(headers, code):
    service = Service()
    with TestClient(create_app(service=service)) as client:
        result = client.put(
            ROUTE, content=serialize(observation()), headers=headers,
        )
    assert result.status_code == code
    assert service.calls == []


def test_query_parameters_are_rejected():
    service = Service()
    with TestClient(create_app(service=service)) as client:
        result = client.put(
            ROUTE + "?token=unexpected",
            content=serialize(observation()), headers=HEADERS,
        )
    assert result.status_code == 400
    assert service.calls == []


def test_real_jwt_save_retry_conflict_and_read_permission_separation(
    tmp_path, keys,
):
    path, service, _, _, _ = setup.environment(tmp_path, keys)
    route = ROUTE.replace("CASE-1", "CASE")
    item = observation(case_id="CASE")
    write_headers = {
        "Authorization": "Bearer " + jwt_setup.token(
            keys[0], operations=(setup.SAVE,),
        ),
        "Content-Type": "application/json",
    }
    read_headers = {
        "Authorization": "Bearer " + jwt_setup.token(
            keys[0], operations=(setup.READ,),
        ),
    }
    with TestClient(create_app(service=service)) as client:
        for _ in range(2):
            assert client.put(
                route, content=serialize(item), headers=write_headers,
            ).status_code == 200
        assert setup.count(path) == 1
        conflict = client.put(
            route, content=serialize(replace(item, description="Changed")),
            headers=write_headers,
        )
        assert conflict.status_code == 409
        assert client.get(route, headers=write_headers).status_code == 403
        recovered = client.get(route, headers=read_headers)
        assert recovered.status_code == 200
        assert recovered.json()["observation_document"] == serialize(item)
        denied = client.put(
            route, content=serialize(item),
            headers={**read_headers, "Content-Type": "application/json"},
        )
        assert denied.status_code == 403
        assert setup.count(path) == 1
