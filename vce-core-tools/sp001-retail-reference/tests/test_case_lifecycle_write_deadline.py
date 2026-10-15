import pytest

from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.services.case_lifecycle_application import (
    open_case, apply_case_lifecycle_transition,
)
import sp001.services.sqlite_case_authoritative_state_store as sqlite_module


class Store:
    def __init__(self):
        self.current = None
        self.deadlines = []
        self.reject = False

    def read(self, *, case_id):
        return self.current

    def read_transitions(self, *, case_id):
        return ()

    def create(self, *, state, transition, write_deadline_ns=None):
        self.deadlines.append(write_deadline_ns)
        if self.reject:
            raise CaseWriteDeadlineExceeded("expired")
        self.current = state
        return True

    def compare_and_swap(
        self, *, expected_revision, next_state, transition,
        write_deadline_ns=None,
    ):
        self.deadlines.append(write_deadline_ns)
        if self.reject:
            raise CaseWriteDeadlineExceeded("expired")
        self.current = next_state
        return True


def open_with(store, deadline=None):
    return open_case(
        store=store, case_id="CASE-001", objective_id="OBJ-001",
        scope="STORE-001", transition_id="T-1",
        write_deadline_ns=deadline,
    )


def advance_with(store, deadline=None):
    return apply_case_lifecycle_transition(
        store=store, case_id="CASE-001", expected_revision=1,
        transition_id="T-2", to_phase=Phase.RECOMMENDATION_AVAILABLE,
        write_deadline_ns=deadline,
    )


def test_same_absolute_deadline_reaches_both_write_operations():
    store = Store()
    assert open_with(store, 123456789).revision == 1
    assert advance_with(store, 123456789).revision == 2
    assert store.deadlines == [123456789, 123456789]


@pytest.mark.parametrize("operation", ["create", "transition"])
def test_deadline_exception_is_not_converted_to_revision_conflict(operation):
    store = Store()
    if operation == "transition":
        open_with(store)
    original = store.current
    store.reject = True
    with pytest.raises(CaseWriteDeadlineExceeded):
        (open_with if operation == "create" else advance_with)(store, 42)
    assert store.current == original


def test_sqlite_keeps_the_same_exception_identity():
    assert sqlite_module.CaseWriteDeadlineExceeded is CaseWriteDeadlineExceeded


def test_application_propagates_expired_deadline_to_real_store(
    tmp_path, monkeypatch,
):
    store = sqlite_module.SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
    )
    monkeypatch.setattr(sqlite_module, "perf_counter_ns", lambda: 200)
    with pytest.raises(CaseWriteDeadlineExceeded):
        open_with(store, 200)
    assert store.read(case_id="CASE-001") is None
    assert store.read_transitions(case_id="CASE-001") == ()

    assert open_with(store, 300).revision == 1
    with pytest.raises(CaseWriteDeadlineExceeded):
        advance_with(store, 200)
    assert store.read(case_id="CASE-001").revision == 1
    assert len(store.read_transitions(case_id="CASE-001")) == 1
    assert advance_with(store, 300).revision == 2
