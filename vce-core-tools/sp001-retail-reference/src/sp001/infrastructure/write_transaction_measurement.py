from time import perf_counter_ns

from sp001.contracts.write_transaction_observation import (
    WriteTransactionObservation,
)


class WriteTransactionMeasurement:
    """Observe existing transaction calls without owning their policy.

    The caller must close its connection before leaving this context.
    Observer exceptions cannot change the transaction result.
    """

    def __init__(self, *, operation, observer):
        self._operation = operation
        self._observer = observer
        self._begin_ns = None
        self._commit_ns = None
        self._rollback_ns = None
        self._committed = False

    def __enter__(self):
        self._started = perf_counter_ns()
        return self

    def begin(self, connection, *, acquisition=None):
        started = perf_counter_ns()
        try:
            if acquisition is not None:
                return acquisition(connection)
            return connection.execute("BEGIN IMMEDIATE")
        finally:
            self._begin_ns = perf_counter_ns() - started

    def commit(self, connection):
        started = perf_counter_ns()
        try:
            result = connection.commit()
            self._committed = True
            return result
        finally:
            self._commit_ns = perf_counter_ns() - started

    def rollback(self, connection):
        started = perf_counter_ns()
        try:
            return connection.rollback()
        finally:
            self._rollback_ns = perf_counter_ns() - started

    def commit_sql(self, connection):
        started = perf_counter_ns()
        try:
            result = connection.execute("COMMIT")
            self._committed = True
            return result
        finally:
            self._commit_ns = perf_counter_ns() - started

    def rollback_sql(self, connection):
        started = perf_counter_ns()
        try:
            return connection.execute("ROLLBACK")
        finally:
            self._rollback_ns = perf_counter_ns() - started

    def __exit__(self, error_type, error, traceback):
        observation = WriteTransactionObservation(
            operation=self._operation,
            begin_ns=self._begin_ns,
            commit_ns=self._commit_ns,
            rollback_ns=self._rollback_ns,
            total_ns=perf_counter_ns() - self._started,
            committed=self._committed,
            failed=error_type is not None,
        )
        if self._observer is not None:
            try:
                self._observer(observation)
            except Exception:
                pass
        return False
