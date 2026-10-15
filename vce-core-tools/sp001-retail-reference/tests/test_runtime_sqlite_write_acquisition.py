import sqlite3
from threading import Event, Thread

import pytest

from sp001.contracts.case_authoritative_state_store import (
    CaseWriteDeadlineExceeded,
)
from sp001.infrastructure.sqlite_write_acquisition import (
    SpacedSqliteWriteAcquisition,
)
from sp001.models.objective import Objective
from sp001.runtime.scientific_product_runtime import ScientificProductRuntime
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
)


def create(runtime, case_id):
    return runtime.create_case(
        Objective(objective_id="OBJ-001"),
        case_id=case_id, scope="STORE-001",
    )


def components(tmp_path, budget_ns):
    path = tmp_path / "case.sqlite3"
    observations = []
    store = SqliteCaseAuthoritativeStateStore(
        database_path=path,
        write_observer=observations.append,
        write_acquisition=SpacedSqliteWriteAcquisition(
            pause_ns=1_000_000,
        ),
    )
    runtime = ScientificProductRuntime(
        case_authoritative_state_store=store,
        case_write_budget_ns=budget_ns,
    )
    return path, store, runtime, observations


def test_runtime_commits_state_and_history_with_optional_acquisition(tmp_path):
    _, store, runtime, observations = components(tmp_path, 2_000_000_000)
    result = create(runtime, "CASE-001")
    assert result.success
    state = store.read(case_id="CASE-001")
    history = store.read_transitions(case_id="CASE-001")
    assert state.revision == 1
    assert len(history) == 1
    assert history[0].case_id == state.case_id
    assert history[0].revision == state.revision
    assert history[0].to_phase is state.phase
    assert len(observations) == 1
    assert observations[0].committed
    assert not observations[0].failed


def test_runtime_expires_while_lock_remains_and_new_request_recovers(tmp_path):
    path, store, runtime, observations = components(tmp_path, 80_000_000)
    finished = Event()
    errors = []

    def work():
        try:
            create(runtime, "EXPIRED")
        except BaseException as error:
            errors.append(error)
        finally:
            finished.set()

    blocker = sqlite3.connect(path, isolation_level=None, timeout=0)
    worker = Thread(target=work)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        worker.start()
        # Watchdog only: this does not assert an 80 ms response guarantee.
        assert finished.wait(3)
        assert len(errors) == 1
        assert isinstance(errors[0], CaseWriteDeadlineExceeded)
        assert store.read(case_id="EXPIRED") is None
        assert store.read_transitions(case_id="EXPIRED") == ()
    finally:
        blocker.execute("ROLLBACK")
        blocker.close()
        if worker.ident is not None:
            worker.join(7)

    assert not worker.is_alive()
    assert len(observations) == 1
    value = observations[0]
    assert value.failed and not value.committed
    assert value.commit_ns is None
    assert value.rollback_ns is None

    # Separate invocation with a fresh budget after releasing the blocker.
    recovery = ScientificProductRuntime(
        case_authoritative_state_store=store,
        case_write_budget_ns=2_000_000_000,
    )
    assert create(recovery, "RECOVERY").success
    assert store.read(case_id="RECOVERY").revision == 1
    assert len(store.read_transitions(case_id="RECOVERY")) == 1
    assert store.read(case_id="EXPIRED") is None
    assert store.read_transitions(case_id="EXPIRED") == ()


def test_runtime_conflict_remains_distinct_from_deadline_expiry(tmp_path):
    _, store, runtime, observations = components(tmp_path, 2_000_000_000)
    assert create(runtime, "CASE-001").success
    original = store.read(case_id="CASE-001")
    history = store.read_transitions(case_id="CASE-001")
    result = create(runtime, "CASE-001")
    assert not result.success
    assert result.output is None
    assert store.read(case_id="CASE-001") == original
    assert store.read_transitions(case_id="CASE-001") == history
    assert len(observations) == 2
    assert not observations[-1].committed
