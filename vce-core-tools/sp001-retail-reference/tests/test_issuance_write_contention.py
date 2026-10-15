from contextlib import contextmanager
import sqlite3
import threading

import pytest

from test_case_access_issuance_completion import components
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    SqliteCaseAccessIssuanceCompletions,
)
from sp001.services.prepared_case_access_completion import (
    PreparedCaseAccessCompleter,
)
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


@pytest.mark.parametrize("expire_while_waiting", [False, True])
def test_real_write_lock_wait_is_measured_and_lifetime_revalidated(
    components, monkeypatch, expire_while_waiting,
):
    path, _, _, _, preparation, signer, protector, _ = components
    observations = []
    store = SqliteCaseAccessIssuanceCompletions(
        database_path=path, write_observer=observations.append,
    )
    now = [150]
    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector,
        clock=lambda: now[0],
    )

    begin_entered = threading.Event()
    finished = threading.Event()
    results = []
    errors = []
    clock_observations = []
    original_connection = store._connection

    class ConnectionProbe:
        """Signals immediately before real BEGIN execution, after timer start."""

        def __init__(self, connection):
            self.connection = connection

        def execute(self, sql, *args):
            if sql == "BEGIN IMMEDIATE":
                begin_entered.set()
            return self.connection.execute(sql, *args)

        def commit(self):
            return self.connection.commit()

        def rollback(self):
            return self.connection.rollback()

    @contextmanager
    def observed_connection():
        with original_connection() as connection:
            yield ConnectionProbe(connection)

    monkeypatch.setattr(store, "_connection", observed_connection)

    def clock():
        clock_observations.append(now[0])
        return now[0]

    # The confirm clock must be sampled only after acquiring the write lock.
    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector, clock=clock,
    )

    def complete():
        try:
            results.append(completer.complete(
                request_id=preparation.request_id,
            ))
        except BaseException as error:
            errors.append(error)
        finally:
            finished.set()

    blocker = sqlite3.connect(path, timeout=0)
    worker = threading.Thread(target=complete, daemon=True)
    try:
        blocker.execute("BEGIN IMMEDIATE")
        worker.start()
        assert begin_entered.wait(2), "worker did not reach BEGIN"

        # SQLite must remain blocked during this deliberately held interval.
        assert not finished.wait(0.15)
        assert clock_observations == []
        assert observations == []

        if expire_while_waiting:
            now[0] = preparation.payload.expires_at

        blocker.rollback()
        worker.join(timeout=4)
        assert not worker.is_alive()
        assert finished.is_set()
    finally:
        blocker.rollback()
        blocker.close()
        if worker.ident is not None:
            worker.join(timeout=6)

    assert not worker.is_alive()
    assert len(observations) == 1
    value = observations[0]
    assert value.operation == "issuance.confirm"
    assert value.begin_ns >= 150_000_000
    assert value.total_ns >= value.begin_ns
    assert clock_observations == [now[0]]

    historical = store.read_completed(request_id=preparation.request_id)
    if expire_while_waiting:
        assert results == []
        assert len(errors) == 1
        assert isinstance(errors[0], IssuanceReferenceValidationError)
        assert historical is None
        assert not value.committed
        assert value.failed
        assert value.commit_ns is None
        assert value.rollback_ns is not None
    else:
        assert errors == []
        assert len(results) == 1
        assert historical is not None
        assert value.committed
        assert not value.failed
        assert value.commit_ns is not None
        assert value.rollback_ns is None

    assert store.read_prepared(
        request_id=preparation.request_id,
    ) == preparation
