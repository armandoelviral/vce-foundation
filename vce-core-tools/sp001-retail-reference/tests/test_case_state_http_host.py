import pytest
from fastapi.testclient import TestClient

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_resource_link import CaseResourceLink
from sp001.contracts.case_state_read_result import Found, NotFound
from sp001.infrastructure.case_state_http_host import (
    CONTRACT_VERSION,
    create_case_state_app,
)


class Reader:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def read(self, *, case_id):
        self.calls.append(case_id)
        if self.error is not None:
            raise self.error
        return self.result


def state(case_id="CASE-001"):
    return CaseAuthoritativeState(
        case_id=case_id,
        objective_id="OBJ-001",
        scope="STORE-001",
        phase=CaseLifecyclePhase.CASE_OPENED,
        revision=8,
        resource_links=(
            CaseResourceLink("evidence", "evidence", "EVD-001"),
        ),
    )


def client(reader, authorize):
    return TestClient(create_case_state_app(reader=reader, authorize=authorize))


def test_found_serializes_complete_state_after_access_check():
    reader = Reader(Found(state()))
    events = []

    def authorize(request, case_id):
        assert reader.calls == []
        events.append((request.method, case_id))
        return True

    with client(reader, authorize) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == {
        "contract_version": CONTRACT_VERSION,
        "code": "CASE_FOUND",
        "case_id": "CASE-001",
        "state": {
            "case_id": "CASE-001",
            "objective_id": "OBJ-001",
            "scope": "STORE-001",
            "phase": "CASE_OPENED",
            "revision": 8,
            "resource_links": [{
                "relationship": "evidence",
                "resource_type": "evidence",
                "resource_id": "EVD-001",
            }],
        },
    }
    assert events == [("GET", "CASE-001")]
    assert reader.calls == ["CASE-001"]


def test_business_404_has_explicit_contract_and_requested_identity():
    reader = Reader(NotFound("CASE-001"))
    with client(reader, lambda request, case_id: True) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 404
    assert response.json() == {
        "contract_version": CONTRACT_VERSION,
        "code": "CASE_NOT_FOUND",
        "case_id": "CASE-001",
    }
    assert response.headers["cache-control"] == "no-store"


def test_route_404_does_not_claim_business_absence():
    reader = Reader(NotFound("CASE-001"))
    with client(reader, lambda request, case_id: True) as http:
        response = http.get("/wrong-route")
    assert response.status_code == 404
    assert response.json().get("code") != "CASE_NOT_FOUND"
    assert reader.calls == []


def test_denied_request_does_not_consult_reader():
    reader = Reader(NotFound("CASE-001"))
    with client(reader, lambda request, case_id: False) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 403
    assert response.json()["code"] == "ACCESS_DENIED"
    assert reader.calls == []


@pytest.mark.parametrize("decision", [None, 0, 1, "yes"])
def test_non_boolean_policy_decision_fails_closed(decision):
    reader = Reader(Found(state()))
    with client(reader, lambda request, case_id: decision) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 500
    assert response.json()["code"] == "INVALID_ACCESS_DECISION"
    assert reader.calls == []


def test_policy_exception_does_not_read_or_expose_details():
    reader = Reader(Found(state()))

    def authorize(request, case_id):
        raise RuntimeError("secret policy detail")

    with client(reader, authorize) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 500
    assert response.json()["code"] == "ACCESS_POLICY_FAILED"
    assert "secret" not in response.text
    assert reader.calls == []


@pytest.mark.parametrize(
    "url",
    [
        "/v1/cases/%20/state",
        "/v1/cases/A/state?case_id=",
        "/v1/cases/A/state?case_id=%20",
        "/v1/cases/A/state?case_id=A&case_id=B",
        "/v1/cases/A/state?unexpected=B",
    ],
)
def test_invalid_query_does_not_read_or_authorize(url):
    reader = Reader(Found(state()))

    def authorize(request, case_id):
        raise AssertionError("must not authorize an invalid request")

    with client(reader, authorize) as http:
        response = http.get(url)
    assert response.status_code == 400
    assert reader.calls == []


@pytest.mark.parametrize(
    "result",
    [Found(state("OTHER")), NotFound("OTHER"), None, {"status": 404}],
)
def test_invalid_reader_result_never_becomes_business_absence(result):
    reader = Reader(result)
    with client(reader, lambda request, case_id: True) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 502
    assert response.json()["code"] == "INVALID_READER_RESPONSE"


def test_reader_failure_is_server_error_without_exception_details():
    reader = Reader(error=RuntimeError("private database path"))
    with client(reader, lambda request, case_id: True) as http:
        response = http.get("/v1/cases/CASE-001/state")
    assert response.status_code == 500
    assert response.json()["code"] == "CASE_READ_FAILED"
    assert "private" not in response.text
    assert reader.calls == ["CASE-001"]


def test_factory_requires_both_dependencies():
    with pytest.raises(TypeError):
        create_case_state_app(reader=Reader())
    with pytest.raises(TypeError):
        create_case_state_app(reader=object(), authorize=lambda r, c: True)
    with pytest.raises(TypeError):
        create_case_state_app(reader=Reader(), authorize=None)


def test_factory_does_not_read_and_apps_do_not_share_readers():
    first = Reader(NotFound("A"))
    second = Reader(NotFound("B"))
    app_a = create_case_state_app(reader=first, authorize=lambda r, c: True)
    app_b = create_case_state_app(reader=second, authorize=lambda r, c: True)
    assert first.calls == second.calls == []
    with TestClient(app_a) as http:
        assert http.get("/v1/cases/A/state").status_code == 404
    assert second.calls == []
    with TestClient(app_b) as http:
        assert http.get("/v1/cases/B/state").status_code == 404
    assert first.calls == ["A"]
    assert second.calls == ["B"]
