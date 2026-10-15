import sqlite3
from threading import Event, Thread

import pytest

from test_sqlite_case_authoritative_state_store import make_state, make_transition
from test_case_state_write_measurement import advance
import sp001.services.sqlite_case_authoritative_state_store as module


def invoke(adapter, operation, deadline):
    if operation == "create":
        return adapter.create(
            state=make_state(), transition=make_transition(),
            write_deadline_ns=deadline,
        )
    from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
    return adapter.compare_and_swap(
        expected_revision=1,
        next_state=make_state(
            phase=Phase.RECOMMENDATION_AVAILABLE, revision=2,
        ),
        transition=make_transition(
            revision=2, from_phase=Phase.CASE_OPENED,
            to_phase=Phase.RECOMMENDATION_AVAILABLE,
        ),
        write_deadline_ns=deadline,
    )


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_expiry_after_real_lock_wait_preserves_state_and_history(
    tmp_path, monkeypatch, operation,
):
    path = tmp_path / "case.sqlite3"
    observations = []
    entered = Event()
    finished = Event()
    now = [100]
    errors = []

    class Probe:
        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            if sql == "BEGIN IMMEDIATE":
                entered.set()
            return self.connection.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(self.connection, name)

    class Store(module.SqliteCaseAuthoritativeStateStore):
        def _connect(self):
            return Probe(super()._connect())

    adapter = Store(database_path=path, write_observer=observations.append)
    if operation == "compare_and_swap":
        assert adapter.create(state=make_state(), transition=make_transition())
    baseline = (
        adapter.read(case_id="CASE-001"),
        adapter.read_transitions(case_id="CASE-001"),
    )
    observations.clear()
    entered.clear()
    monkeypatch.setattr(module, "perf_counter_ns", lambda: now[0])

    def work():
        try:
            invoke(adapter, operation, 200)
        except BaseException as error:
            errors.append(error)
        finally:
            finished.set()

    blocker = sqlite3.connect(path, timeout=0)
    worker = Thread(target=work)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        worker.start()
        assert entered.wait(2)
        assert not finished.is_set()
        # Deterministic budget expiry while the independent writer owns the lock.
        now[0] = 200
    finally:
        blocker.rollback()
        blocker.close()
        if worker.ident is not None:
            worker.join(7)

    assert not worker.is_alive()
    assert finished.is_set()
    assert len(errors) == 1
    assert isinstance(errors[0], module.CaseWriteDeadlineExceeded)
    assert (
        adapter.read(case_id="CASE-001"),
        adapter.read_transitions(case_id="CASE-001"),
    ) == baseline
    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.begin_ns is not None
    assert value.rollback_ns is not None
    assert value.commit_ns is None

    assert invoke(adapter, operation, 300)
    assert adapter.read(case_id="CASE-001").revision == (
        1 if operation == "create" else 2
    )
    assert len(adapter.read_transitions(case_id="CASE-001")) == (
        1 if operation == "create" else 2
    )


@pytest.mark.parametrize("operation", ["create", "compare_and_swap"])
def test_expiry_before_commit_rolls_back_both_tables(
    tmp_path, monkeypatch, operation,
):
    adapter = module.SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
    )
    if operation == "compare_and_swap":
        assert adapter.create(state=make_state(), transition=make_transition())
    baseline = (
        adapter.read(case_id="CASE-001"),
        adapter.read_transitions(case_id="CASE-001"),
    )
    # Before connection, after BEGIN, immediately before COMMIT.
    times = iter((100, 100, 200))
    monkeypatch.setattr(module, "perf_counter_ns", lambda: next(times))
    with pytest.raises(module.CaseWriteDeadlineExceeded):
        invoke(adapter, operation, 200)
    assert (
        adapter.read(case_id="CASE-001"),
        adapter.read_transitions(case_id="CASE-001"),
    ) == baseline


def test_expired_budget_opens_no_connection(tmp_path, monkeypatch):
    adapter = module.SqliteCaseAuthoritativeStateStore(
        database_path=tmp_path / "case.sqlite3",
    )
    monkeypatch.setattr(module, "perf_counter_ns", lambda: 200)

    def forbidden(self):
        raise AssertionError("connection must not be opened")

    monkeypatch.setattr(type(adapter), "_connect", forbidden)
    with pytest.raises(module.CaseWriteDeadlineExceeded):
        invoke(adapter, "create", 200)
