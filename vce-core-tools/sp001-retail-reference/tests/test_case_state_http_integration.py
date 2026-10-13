import pytest
from fastapi.testclient import TestClient

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_state_read_result import Found, NotFound
from sp001.infrastructure.case_state_http_host import create_case_state_app
from sp001.infrastructure import remote_case_state_reader as remote
from sp001.services.case_state_reconciliation import ViewStatus
from sp001.services.case_state_subscription import CaseStateSubscription


def state(revision):
    return CaseAuthoritativeState(
        case_id="CASE-001",
        objective_id="OBJ-001",
        scope="STORE-001",
        phase=CaseLifecyclePhase.CASE_OPENED,
        revision=revision,
        resource_links=(),
    )


class HostReader:
    def __init__(self):
        self.result = Found(state(8))
        self.error = None
        self.calls = []

    def read(self, *, case_id):
        self.calls.append(case_id)
        if self.error is not None:
            raise self.error
        return self.result


@pytest.fixture
def chain(monkeypatch):
    host_reader = HostReader()
    access = {"allowed": True}
    bridge = {"route_override": None}
    requests = []
    app = create_case_state_app(
        reader=host_reader,
        authorize=lambda request, case_id: access["allowed"],
    )

    with TestClient(app) as http:
        class WireResponse:
            def __init__(self, response):
                self.status = response.status_code
                self.headers = response.headers
                self.body = response.content

            def getheader(self, name, default=None):
                return self.headers.get(name, default)

            def read(self, limit):
                return self.body[:limit]

        class Connection:
            def __init__(self, *args, **kwargs):
                self.response = None

            def request(self, method, target, headers):
                requests.append((method, target))
                route = bridge["route_override"] or target
                self.response = http.request(
                    method, route, headers=headers, follow_redirects=False
                )

            def getresponse(self):
                return WireResponse(self.response)

            def close(self):
                pass

        monkeypatch.setattr(remote.http.client, "HTTPSConnection", Connection)
        reader = remote.RemoteCaseStateReader(
            endpoint="https://coordinator.example/v1/case-state",
            timeout_seconds=1,
            max_response_bytes=4096,
        )
        subscription = CaseStateSubscription(
            reader=reader, case_id="CASE-001"
        )
        yield host_reader, access, bridge, requests, subscription


def test_found_idempotence_regression_and_update_through_http(chain):
    host, access, bridge, requests, subscription = chain
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    original = view.last_valid_state
    assert original.revision == 8

    host.result = Found(state(8))
    assert subscription.refresh().last_valid_state is original

    host.result = Found(state(7))
    view = subscription.refresh()
    assert view.status is ViewStatus.STALE_RESPONSE
    assert view.last_valid_state is original

    host.result = Found(state(9))
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state.revision == 9
    assert len(requests) == 4
    assert host.calls == ["CASE-001"] * 4


def test_business_404_and_route_404_have_different_effects(chain):
    host, access, bridge, requests, subscription = chain
    original = subscription.refresh().last_valid_state

    host.result = NotFound("CASE-001")
    view = subscription.refresh()
    assert view.status is ViewStatus.NOT_FOUND
    assert view.last_valid_state is original

    bridge["route_override"] = "/wrong-route"
    count = len(host.calls)
    view = subscription.refresh()
    assert view.status is ViewStatus.INVALID_RESPONSE
    assert view.last_valid_state is original
    assert len(host.calls) == count
    assert len(requests) == 3


def test_denied_access_does_not_read_and_retains_previous_state(chain):
    host, access, bridge, requests, subscription = chain
    original = subscription.refresh().last_valid_state
    count = len(host.calls)
    access["allowed"] = False
    view = subscription.refresh()
    assert view.status is ViewStatus.REQUEST_REJECTED
    assert view.last_valid_state is original
    assert len(host.calls) == count
    assert len(requests) == 2


def test_host_failure_is_unavailability_not_absence_and_can_recover(chain):
    host, access, bridge, requests, subscription = chain
    original = subscription.refresh().last_valid_state
    host.error = RuntimeError("private storage detail")
    view = subscription.refresh()
    assert view.status is ViewStatus.UNAVAILABLE
    assert view.last_valid_state is original
    assert view.reason == "backend_status:500"
    assert "private" not in view.reason

    host.error = None
    host.result = Found(state(9))
    view = subscription.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state.revision == 9
    assert len(requests) == 3
