import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.services.case_authoritative_state_reading import (
    read_case_authoritative_state,
)


class StubStore:
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
        raise AssertionError("reading must not create")

    def compare_and_swap(self, *, expected_revision, next_state, transition):
        raise AssertionError("reading must not mutate")

    def read_transitions(self, *, case_id):
        raise AssertionError("reading must not query history")


def state(case_id="CASE-001"):
    return CaseAuthoritativeState(
        case_id=case_id,
        objective_id="OBJ-001",
        scope="STORE-MX-014",
        phase=CaseLifecyclePhase.CASE_OPENED,
        revision=1,
        resource_links=(),
    )


def test_found_preserves_exact_state_and_requested_identity():
    expected = state()
    store = StubStore(result=expected)
    assert read_case_authoritative_state(
        store=store, case_id="CASE-001"
    ) is expected
    assert store.calls == ["CASE-001"]


def test_successful_missing_read_returns_none():
    store = StubStore()
    assert read_case_authoritative_state(
        store=store, case_id="MISSING"
    ) is None
    assert store.calls == ["MISSING"]


def test_different_case_identity_is_rejected():
    store = StubStore(result=state("CASE-OTHER"))
    with pytest.raises(ValueError, match="different case_id"):
        read_case_authoritative_state(store=store, case_id="CASE-001")


def test_invalid_store_response_is_not_missing():
    store = StubStore(result={"case_id": "CASE-001"})
    with pytest.raises(TypeError, match="store.read must return"):
        read_case_authoritative_state(store=store, case_id="CASE-001")


@pytest.mark.parametrize(
    "error",
    [TimeoutError("timeout"), ConnectionError("connection interrupted")],
)
def test_read_failure_propagates_instead_of_becoming_missing(error):
    store = StubStore(error=error)
    with pytest.raises(type(error)) as caught:
        read_case_authoritative_state(store=store, case_id="CASE-001")
    assert caught.value is error
    assert store.calls == ["CASE-001"]


@pytest.mark.parametrize("case_id", [None, 1, True, "", "   "])
def test_invalid_request_never_calls_store(case_id):
    store = StubStore()
    with pytest.raises((TypeError, ValueError)):
        read_case_authoritative_state(store=store, case_id=case_id)
    assert store.calls == []


def test_invalid_store_is_rejected():
    with pytest.raises(TypeError, match="must implement"):
        read_case_authoritative_state(store=object(), case_id="CASE-001")
