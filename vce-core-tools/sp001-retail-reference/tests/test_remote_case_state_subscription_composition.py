import pytest

from test_case_state_https_loopback import https_host
from test_remote_case_state_reader import install_connection, Response
from sp001.infrastructure.remote_case_state_subscription_composition import (
    compose_remote_case_state_subscription,
)
from sp001.services.case_state_reconciliation import (
    SessionResponseRejected, ViewStatus,
)


def compose(**changes):
    configuration = {
        "endpoint": "https://coordinator.example/v1/cases/{caseId}/state",
        "case_id": "CASE-001",
        "credential_provider": lambda: "credential",
        "timeout_seconds": 1,
        "max_response_bytes": 4096,
    }
    configuration.update(changes)
    return compose_remote_case_state_subscription(**configuration)


def test_composition_performs_no_network_or_credential_call(monkeypatch):
    calls = install_connection(monkeypatch)

    def forbidden_credential():
        raise AssertionError("composition must not obtain credentials")

    session = compose(credential_provider=forbidden_credential)
    assert session.view.status is ViewStatus.UNCONFIRMED
    assert calls == []


@pytest.mark.parametrize("status", [401, 403])
def test_http_rejection_terminates_composed_session(monkeypatch, status):
    class Rejection(Response):
        pass

    response = Rejection()
    response.status = status
    calls = install_connection(monkeypatch, response=response)
    session = compose()
    blocked = session.refresh()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.last_valid_state is None
    before = list(calls)
    with pytest.raises(SessionResponseRejected):
        session.refresh()
    assert calls == before


def test_success_then_403_withdraws_composed_snapshot(monkeypatch):
    response = Response()
    calls = install_connection(monkeypatch, response=response)
    session = compose(clock=lambda: 100)
    assert session.refresh().last_valid_state is not None
    response.status = 403
    blocked = session.refresh()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.last_valid_state is None
    assert len([call for call in calls if call[0] == "request"]) == 2


def test_real_https_snapshot_expires_through_composed_session(https_host):
    port, ca, source = https_host
    now = [100.0]
    session = compose(
        endpoint=f"https://localhost:{port}/v1/cases/{{caseId}}/state",
        ca_file=str(ca), clock=lambda: now[0],
    )
    assert source.calls == []
    view = session.refresh()
    assert view.status is ViewStatus.CURRENT
    assert view.last_valid_state == source.state
    now[0] = 110.0
    blocked = session.tick()
    assert blocked.status is ViewStatus.BLOCKED
    assert blocked.last_valid_state is None
    with pytest.raises(SessionResponseRejected):
        session.refresh()
    assert source.calls == ["CASE-001"]


@pytest.mark.parametrize("changes", [
    {"case_id": "A/B"},
    {"credential_provider": None},
    {"clock": 123},
    {"endpoint": "https://coordinator.example/v1/case-state"},
])
def test_invalid_configuration_is_rejected(changes):
    with pytest.raises((TypeError, ValueError)):
        compose(**changes)
