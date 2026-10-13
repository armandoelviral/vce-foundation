import json
import ssl

import pytest

from sp001.contracts.case_state_read_result import (
    BackendUnavailable, Found, InvalidResponse, NotFound,
    RequestRejected, TransportUnavailable,
)
from sp001.infrastructure import remote_case_state_reader as module
from sp001.services.case_state_subscription import CaseStateSubscription


def payload():
    return {
        "contract_version": module.CONTRACT_VERSION,
        "code": "CASE_FOUND",
        "case_id": "CASE-001",
        "state": {
            "case_id": "CASE-001",
            "objective_id": "OBJ-001",
            "scope": "",
            "phase": "CASE_OPENED",
            "revision": 8,
            "resource_links": [],
        },
    }


def classify(value, status=200, content_type="application/json"):
    return module.classify_case_state_response(
        case_id="CASE-001",
        status_code=status,
        content_type=content_type,
        body=json.dumps(value).encode(),
    )


def test_found_reconstructs_validated_state():
    result = classify(payload())
    assert isinstance(result, Found)
    assert result.state.revision == 8
    assert result.state.case_id == "CASE-001"


def test_only_explicit_business_404_becomes_not_found():
    assert classify({
        "contract_version": module.CONTRACT_VERSION,
        "code": "CASE_NOT_FOUND",
        "case_id": "CASE-001",
    }, 404) == NotFound("CASE-001")


@pytest.mark.parametrize(
    "value",
    [
        {"detail": "Not Found"},
        {},
        {"contract_version": "unknown", "code": "CASE_NOT_FOUND", "case_id": "CASE-001"},
        {"contract_version": module.CONTRACT_VERSION, "code": "CASE_NOT_FOUND", "case_id": "OTHER"},
        {"contract_version": module.CONTRACT_VERSION, "code": "CASE_FOUND", "case_id": "CASE-001"},
    ],
)
def test_infrastructure_or_invalid_404_is_not_absence(value):
    assert isinstance(classify(value, 404), InvalidResponse)


@pytest.mark.parametrize("body", [b"", b"<html>404</html>", b"{", b"\xff"])
def test_unreadable_404_is_invalid_response(body):
    result = module.classify_case_state_response(
        case_id="CASE-001", status_code=404,
        content_type="application/json", body=body,
    )
    assert isinstance(result, InvalidResponse)


@pytest.mark.parametrize(
    "field,value",
    [
        ("case_id", "OTHER"),
        ("objective_id", ""),
        ("scope", None),
        ("phase", "UNKNOWN"),
        ("revision", True),
        ("revision", "8"),
        ("revision", 0),
        ("resource_links", {}),
    ],
)
def test_invalid_state_fields_are_rejected(field, value):
    body = payload()
    body["state"][field] = value
    assert isinstance(classify(body), InvalidResponse)


def test_extra_fields_duplicate_keys_and_nonstandard_numbers_are_rejected():
    body = payload()
    body["extra"] = True
    assert isinstance(classify(body), InvalidResponse)
    for raw in (b'{"code":"A","code":"B"}', b'{"revision":NaN}'):
        assert isinstance(module.classify_case_state_response(
            case_id="CASE-001", status_code=200,
            content_type="application/json", body=raw,
        ), InvalidResponse)


@pytest.mark.parametrize("status", [429, 500, 503, 599])
def test_backend_unavailability_is_separate(status):
    assert isinstance(classify({}, status), BackendUnavailable)


@pytest.mark.parametrize("status", [400, 401, 403, 422])
def test_request_rejection_is_separate(status):
    assert isinstance(classify({}, status), RequestRejected)


@pytest.mark.parametrize("status", [204, 301, 302, 307])
def test_other_statuses_and_redirects_are_invalid(status):
    assert isinstance(classify({}, status), InvalidResponse)


def reader():
    return module.RemoteCaseStateReader(
        endpoint="https://coordinator.example/v1/case-state",
        timeout_seconds=1,
        max_response_bytes=4096,
    )


class Response:
    status = 200

    def getheader(self, name, default=None):
        return {"Content-Type": "application/json"}.get(name, default)

    def read(self, limit):
        return json.dumps(payload()).encode()[:limit]


def install_connection(monkeypatch, response=None, error=None):
    calls = []

    class Connection:
        def __init__(self, *args, **kwargs):
            calls.append(("connection", kwargs))

        def request(self, method, target, headers):
            calls.append(("request", method, target))
            if error is not None:
                raise error

        def getresponse(self):
            return response or Response()

        def close(self):
            calls.append(("close",))

    monkeypatch.setattr(module.http.client, "HTTPSConnection", Connection)
    return calls


def test_remote_reader_feeds_subscription_without_retry(monkeypatch):
    calls = install_connection(monkeypatch)
    subscription = CaseStateSubscription(reader=reader(), case_id="CASE-001")
    view = subscription.refresh()
    assert view.status == "CURRENT"
    assert view.last_valid_state.revision == 8
    assert len([c for c in calls if c[0] == "request"]) == 1
    context = calls[0][1]["context"]
    assert context.check_hostname
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert calls[-1] == ("close",)


@pytest.mark.parametrize(
    "error,expected",
    [
        (TimeoutError("timeout"), TransportUnavailable),
        (ConnectionError("connection lost"), TransportUnavailable),
        (ssl.SSLCertVerificationError("certificate"), InvalidResponse),
    ],
)
def test_transport_failures_are_not_absence_and_do_not_retry(monkeypatch, error, expected):
    calls = install_connection(monkeypatch, error=error)
    assert isinstance(reader().read(case_id="CASE-001"), expected)
    assert len([c for c in calls if c[0] == "request"]) == 1
    assert calls[-1] == ("close",)


def test_response_limit_is_enforced(monkeypatch):
    class LargeResponse(Response):
        def read(self, limit):
            return b"x" * limit

    install_connection(monkeypatch, response=LargeResponse())
    assert reader().read(case_id="CASE-001") == InvalidResponse(
        "response_size_limit_exceeded"
    )


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://coordinator.example/v1/case-state",
        "https://user:password@coordinator.example/v1/case-state",
        "https://coordinator.example/wrong",
        "https://coordinator.example/v1/case-state?case_id=A",
        "https://coordinator.example/v1/case-state#fragment",
    ],
)
def test_invalid_endpoint_is_rejected(endpoint):
    with pytest.raises(ValueError):
        module.RemoteCaseStateReader(
            endpoint=endpoint, timeout_seconds=1, max_response_bytes=4096
        )
