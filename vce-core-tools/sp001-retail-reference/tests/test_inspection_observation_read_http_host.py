from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from test_retail_inspection_observation import observation
from sp001.infrastructure.inspection_observation_read_http_host import (
    create_inspection_observation_read_app,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_authorized_inspection_observations import (
    InspectionObservationAuthenticationRejected as Rejected,
    InspectionObservationAccessDenied as Denied,
)


ROUTE = "/v1/cases/CASE-1/inspection-observations/OBS-1/versions/1"
HEADERS = {"Authorization": "Bearer synthetic-credential"}


class Service:
    """HTTP boundary double; does not authenticate or persist."""

    def __init__(self, *replies):
        self.replies = iter(replies)
        self.calls = []

    def recover(self, **arguments):
        self.calls.append(arguments)
        reply = next(self.replies)
        if isinstance(reply, Exception):
            raise reply
        return reply


def client(service, **kwargs):
    return TestClient(create_inspection_observation_read_app(
        service=service, **kwargs,
    ))


def test_exact_recovery_and_final_authenticated_query():
    item = observation()
    service = Service(item, item)
    with client(service) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == 200
    assert result.json() == {
        "status": "ok", "observation_document": serialize(item),
    }
    assert result.headers["cache-control"] == "no-store"
    assert len(service.calls) == 2
    assert service.calls[0] == service.calls[1]
    assert service.calls[0]["identity"].observation_version == 1
    assert service.calls[0]["case_id"] == "CASE-1"


@pytest.mark.parametrize("reply,code,status", [
    (None, 404, "observation_not_found"),
    (Rejected("private credential detail"), 401, "credential_rejected"),
    (Denied("private grant detail"), 403, "access_denied"),
    (OSError("private storage detail"), 503, "backend_unavailable"),
])
def test_distinguishes_absence_rejection_denial_and_failure(reply, code, status):
    with client(Service(reply)) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == code
    assert result.json() == {"status": status}
    assert result.headers["cache-control"] == "no-store"
    assert "private" not in result.text
    assert "synthetic-credential" not in result.text


@pytest.mark.parametrize("reply,code,status", [
    (Rejected("expired during preparation"), 401, "credential_rejected"),
    (Denied("revoked during preparation"), 403, "access_denied"),
    (OSError("backend failed"), 503, "backend_unavailable"),
    (None, 503, "backend_unavailable"),
    ("invalid return", 503, "backend_unavailable"),
])
def test_final_query_error_never_returns_prepared_content(reply, code, status):
    item = observation(description="SENSITIVE OBSERVATION")
    with client(Service(item, reply)) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == code
    assert result.json() == {"status": status}
    assert "SENSITIVE" not in result.text


def test_content_change_during_preparation_is_not_exported():
    original = observation()
    changed = replace(original, description="Changed content.")
    with client(Service(original, changed)) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == 503
    assert result.json() == {"status": "backend_unavailable"}


@pytest.mark.parametrize("reply,code", [
    ("invalid", 503),
    (replace(observation(), observation_id="OTHER"), 503),
    (replace(observation(), observation_version=2), 503),
    (replace(observation(), case_id="OTHER"), 403),
])
def test_rejects_inconsistent_service_result(reply, code):
    with client(Service(reply)) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == code
    assert "observation_document" not in result.json()


@pytest.mark.parametrize("headers", [
    {}, {"Authorization": "Basic value"},
    {"Authorization": "Bearer"},
    {"Authorization": "Bearer one two"},
    [("Authorization", "Bearer one"), ("Authorization", "Bearer two")],
])
def test_invalid_authorization_never_calls_service(headers):
    service = Service()
    with client(service) as http:
        result = http.get(ROUTE, headers=headers)
    assert result.status_code == 401
    assert result.json() == {"status": "credential_rejected"}
    assert service.calls == []


def test_oversized_token_is_rejected_before_service():
    service = Service()
    with client(service, max_token_bytes=3) as http:
        result = http.get(ROUTE, headers=HEADERS)
    assert result.status_code == 401
    assert service.calls == []


@pytest.mark.parametrize("version", ["0", "-1", "01", "abc", "1.0"])
def test_invalid_version_never_calls_service(version):
    service = Service()
    with client(service) as http:
        result = http.get(
            ROUTE.rsplit("/", 1)[0] + "/" + version, headers=HEADERS,
        )
    assert result.status_code == 400
    assert result.json() == {"status": "invalid_request"}
    assert service.calls == []


@pytest.mark.parametrize("value,error", [
    (True, TypeError), (0, ValueError), (-1, ValueError),
])
def test_invalid_token_limit(value, error):
    with pytest.raises(error):
        create_inspection_observation_read_app(
            service=Service(), max_token_bytes=value,
        )


def test_invalid_service_is_rejected():
    with pytest.raises(TypeError):
        create_inspection_observation_read_app(service=object())
