import pytest
from fastapi.testclient import TestClient

import time
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import (
    ValidatedCaseAccessContext, CaseAccessPermission, CaseAccessOperation,
)
from sp001.contracts.case_state_read_result import NotFound
from sp001.infrastructure.authenticated_case_state_http_host import (
    create_authenticated_case_state_app,
)


class Authenticator:
    def __init__(self, events):
        self.events = events
        now = int(time.time())
        self.result = ValidatedCaseAccessContext(
            principal=AuthenticatedPrincipal("issuer-A", "subscriber-1"),
            audience="sp001-coordinator",
            issued_at=now - 1, not_before=now - 1, expires_at=now + 300,
            permissions=(
                CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE),
            ),
        )
        self.error = None

    def authenticate(self, *, credential):
        self.events.append("authenticate")
        if self.error is not None:
            raise self.error
        return self.result if credential == "test-credential" else None


class Authorizer:
    def __init__(self, events):
        self.events = events
        self.result = True
        self.error = None
        self.calls = []

    def can_read_case(self, *, access, case_id):
        self.events.append("authorize")
        self.calls.append((access, case_id))
        if self.error is not None:
            raise self.error
        return self.result


class Reader:
    def __init__(self, events):
        self.events = events
        self.calls = []

    def read(self, *, case_id):
        self.events.append("read")
        self.calls.append(case_id)
        return NotFound(case_id)


@pytest.fixture
def setup():
    events = []
    authenticator = Authenticator(events)
    authorizer = Authorizer(events)
    reader = Reader(events)
    app = create_authenticated_case_state_app(
        expected_audience="sp001-coordinator",
        reader=reader, authenticator=authenticator, authorizer=authorizer
    )
    with TestClient(app) as client:
        yield client, authenticator, authorizer, reader, events


def request(client, headers=None):
    return client.get(
        "/v1/case-state", params={"case_id": "CASE-001"}, headers=headers
    )


HEADERS = {"Authorization": "Bearer test-credential"}


@pytest.mark.parametrize(
    "headers",
    [
        None,
        {"Authorization": ""},
        {"Authorization": "Basic test-credential"},
        {"Authorization": "Bearer"},
        {"Authorization": "Bearer test credential"},
        [("Authorization", "Bearer A"), ("Authorization", "Bearer B")],
    ],
)
def test_missing_or_malformed_credentials_do_not_authorize_or_read(setup, headers):
    client, authenticator, authorizer, reader, events = setup
    response = request(client, headers)
    assert response.status_code == 401
    assert response.headers["www-authenticate"].startswith("Bearer")
    assert response.headers["cache-control"] == "no-store"
    assert events == []


def test_invalid_credential_does_not_authorize_or_read(setup):
    client, authenticator, authorizer, reader, events = setup
    response = request(client, {"Authorization": "Bearer wrong"})
    assert response.status_code == 401
    assert events == ["authenticate"]
    assert reader.calls == []


def test_exact_principal_and_case_are_authorized_before_read(setup):
    client, authenticator, authorizer, reader, events = setup
    response = request(client, HEADERS)
    assert response.status_code == 404
    assert response.json()["code"] == "CASE_NOT_FOUND"
    assert events == ["authenticate", "authorize", "read"]
    principal, case_id = authorizer.calls[0]
    assert principal is authenticator.result
    assert case_id == "CASE-001"


def test_authenticated_but_denied_is_403_without_existence_lookup(setup):
    client, authenticator, authorizer, reader, events = setup
    authorizer.result = False
    response = request(client, HEADERS)
    assert response.status_code == 403
    assert response.json()["code"] == "ACCESS_DENIED"
    assert events == ["authenticate", "authorize"]
    assert reader.calls == []


@pytest.mark.parametrize("value", [False, True, {}, "subscriber-1"])
def test_invalid_authentication_result_fails_closed(setup, value):
    client, authenticator, authorizer, reader, events = setup
    authenticator.result = value
    response = request(client, HEADERS)
    assert response.status_code == 500
    assert response.json()["code"] == "INVALID_AUTHENTICATION_RESULT"
    assert events == ["authenticate"]


def test_authenticator_failure_is_not_invalid_credentials(setup):
    client, authenticator, authorizer, reader, events = setup
    authenticator.error = RuntimeError("private provider detail")
    response = request(client, HEADERS)
    assert response.status_code == 500
    assert response.json()["code"] == "AUTHENTICATION_PROVIDER_FAILED"
    assert "private" not in response.text
    assert events == ["authenticate"]


@pytest.mark.parametrize("value", [None, 1, "yes"])
def test_invalid_authorization_result_fails_closed(setup, value):
    client, authenticator, authorizer, reader, events = setup
    authorizer.result = value
    response = request(client, HEADERS)
    assert response.status_code == 500
    assert response.json()["code"] == "INVALID_ACCESS_DECISION"
    assert reader.calls == []


def test_authorizer_failure_does_not_read_or_disclose_details(setup):
    client, authenticator, authorizer, reader, events = setup
    authorizer.error = RuntimeError("private access detail")
    response = request(client, HEADERS)
    assert response.status_code == 500
    assert response.json()["code"] == "ACCESS_POLICY_FAILED"
    assert "private" not in response.text
    assert reader.calls == []


def test_unknown_route_is_not_business_absence(setup):
    client, authenticator, authorizer, reader, events = setup
    response = client.get("/wrong-route")
    assert response.status_code == 404
    assert response.json().get("code") != "CASE_NOT_FOUND"
    assert events == []


def test_access_is_checked_on_every_request(setup):
    client, authenticator, authorizer, reader, events = setup
    assert request(client, HEADERS).status_code == 404
    authorizer.result = False
    assert request(client, HEADERS).status_code == 403
    assert reader.calls == ["CASE-001"]
    assert events == [
        "authenticate", "authorize", "read",
        "authenticate", "authorize",
    ]


def test_factory_requires_valid_security_ports():
    with pytest.raises(TypeError):
        create_authenticated_case_state_app(
        expected_audience="sp001-coordinator",
            reader=Reader([]), authenticator=object(), authorizer=Authorizer([])
        )
    with pytest.raises(TypeError):
        create_authenticated_case_state_app(
        expected_audience="sp001-coordinator",
            reader=Reader([]), authenticator=Authenticator([]), authorizer=object()
        )
