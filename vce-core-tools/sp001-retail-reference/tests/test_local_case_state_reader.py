from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_state_read_result import (
    BackendUnavailable,
    Found,
    InvalidResponse,
    NotFound,
    RequestRejected,
    TransportUnavailable,
)
from sp001.contracts.case_state_reader import CaseStateReader
from sp001.services.local_case_state_reader import LocalCaseStateReader


class Store:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def read(self, *, case_id):
        self.calls.append(case_id)
        if self.error is not None:
            raise self.error
        return self.result

    def create(self, *, state, transition):
        raise AssertionError("unexpected mutation")

    def compare_and_swap(self, *, expected_revision, next_state, transition):
        raise AssertionError("unexpected mutation")

    def read_transitions(self, *, case_id):
        raise AssertionError("unexpected history read")


def state(case_id="CASE-001"):
    return CaseAuthoritativeState(
        case_id=case_id,
        objective_id="OBJ-001",
        scope="",
        phase=CaseLifecyclePhase.CASE_OPENED,
        revision=1,
        resource_links=(),
    )


def test_found_preserves_exact_state():
    expected = state()
    reader = LocalCaseStateReader(store=Store(result=expected))
    assert isinstance(reader, CaseStateReader)
    result = reader.read(case_id="CASE-001")
    assert isinstance(result, Found)
    assert result.state is expected


def test_successful_absence_is_explicit():
    reader = LocalCaseStateReader(store=Store())
    assert reader.read(case_id="MISSING") == NotFound(case_id="MISSING")


@pytest.mark.parametrize(
    "error",
    [TimeoutError("timeout"), RuntimeError("storage failure")],
)
def test_local_failures_are_not_domain_absence(error):
    store = Store(error=error)
    reader = LocalCaseStateReader(store=store)
    with pytest.raises(type(error)) as caught:
        reader.read(case_id="CASE-001")
    assert caught.value is error
    assert store.calls == ["CASE-001"]


def test_identity_mismatch_is_not_domain_absence():
    reader = LocalCaseStateReader(store=Store(result=state("OTHER")))
    with pytest.raises(ValueError, match="different case_id"):
        reader.read(case_id="CASE-001")


def test_invalid_response_is_not_domain_absence():
    reader = LocalCaseStateReader(store=Store(result={}))
    with pytest.raises(TypeError, match="store.read must return"):
        reader.read(case_id="CASE-001")


@pytest.mark.parametrize("case_id", [None, 1, True, "", " "])
def test_invalid_request_does_not_call_store(case_id):
    store = Store()
    reader = LocalCaseStateReader(store=store)
    with pytest.raises((TypeError, ValueError)):
        reader.read(case_id=case_id)
    assert store.calls == []


def test_invalid_store_is_rejected():
    with pytest.raises(TypeError):
        LocalCaseStateReader(store=object())


@pytest.mark.parametrize(
    "factory",
    [NotFound, TransportUnavailable, InvalidResponse],
)
@pytest.mark.parametrize("value", [None, 1, True, "", " "])
def test_text_outcomes_reject_invalid_values(factory, value):
    with pytest.raises((TypeError, ValueError)):
        factory(value)


def test_found_rejects_untyped_state():
    with pytest.raises(TypeError):
        Found(state={})


@pytest.mark.parametrize("code", [429, 500, 503, 599])
def test_backend_unavailable_accepts_only_declared_statuses(code):
    assert BackendUnavailable(status_code=code).status_code == code


@pytest.mark.parametrize("code", [None, True, "503", 404, 400, 499, 600])
def test_backend_unavailable_rejects_other_statuses(code):
    with pytest.raises((TypeError, ValueError)):
        BackendUnavailable(status_code=code)


@pytest.mark.parametrize("code", [400, 401, 403, 422])
def test_request_rejected_preserves_status_and_reason(code):
    result = RequestRejected(status_code=code, reason="request rejected")
    assert result.status_code == code
    assert result.reason == "request rejected"


@pytest.mark.parametrize("code", [None, True, "403", 399, 404, 429, 500])
def test_request_rejected_cannot_absorb_404_or_unavailability(code):
    with pytest.raises((TypeError, ValueError)):
        RequestRejected(status_code=code, reason="rejected")


@pytest.mark.parametrize("reason", [None, 1, "", " "])
def test_request_rejected_requires_reason(reason):
    with pytest.raises((TypeError, ValueError)):
        RequestRejected(status_code=403, reason=reason)


@pytest.mark.parametrize(
    "result",
    [
        Found(state=state()),
        NotFound(case_id="CASE-001"),
        TransportUnavailable(cause="timeout"),
        BackendUnavailable(status_code=503),
        InvalidResponse(reason="unrecognized infrastructure 404"),
        RequestRejected(status_code=403, reason="forbidden"),
    ],
)
def test_outcomes_are_immutable_and_slotted(result):
    field = next(iter(result.__dataclass_fields__))
    with pytest.raises(FrozenInstanceError):
        setattr(result, field, None)
    assert not hasattr(result, "__dict__")
