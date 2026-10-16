import sqlite3
from time import perf_counter_ns

from sp001.contracts.case_authoritative_state_store import CaseWriteDeadlineExceeded
from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)
from sp001.contracts.case_lifecycle_transition_record import CaseLifecycleTransitionRecord
from sp001.infrastructure.case_lifecycle_serialization import (
    serialize_case_lifecycle, deserialize_case_lifecycle,
)
from sp001.infrastructure.write_transaction_measurement import WriteTransactionMeasurement
from sp001.services.case_lifecycle_application import (
    open_case, apply_case_lifecycle_transition,
)
from sp001.services.case_lifecycle_recovery import match_case_lifecycle_completion
from sp001.services.sqlite_case_authoritative_state_store import (
    SqliteCaseAuthoritativeStateStore,
    _check_write_deadline, _configure_write_wait, _revision_text, _serialize_links,
)


class _TransactionView:
    """Private persistence capability bound to an already-open transaction."""

    def __init__(self, owner, connection):
        self.owner = owner
        self.connection = connection
        self.previous = None
        self.record = None

    def read(self, *, case_id):
        row = self.connection.execute(
            "SELECT * FROM case_authoritative_states WHERE case_id=?",
            (case_id,),
        ).fetchone()
        return None if row is None else self.owner._state_from_row(row)

    def read_transitions(self, *, case_id):
        rows = self.connection.execute(
            "SELECT * FROM case_lifecycle_transitions WHERE case_id=? ORDER BY revision",
            (case_id,),
        ).fetchall()
        return tuple(self.owner._transition_from_row(row) for row in rows)

    def _append(self, transition):
        self.connection.execute(
            """INSERT INTO case_lifecycle_transitions
            (case_id, revision, transition_id, from_phase, to_phase,
             resource_links_serialization) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                transition.case_id, _revision_text(transition.revision),
                transition.transition_id,
                None if transition.from_phase is None else transition.from_phase.value,
                transition.to_phase.value,
                _serialize_links(transition.resource_links),
            ),
        )
        self.record = transition

    def create(self, *, state, transition):
        if self.read(case_id=state.case_id) is not None:
            return False
        self.connection.execute(
            """INSERT INTO case_authoritative_states
            (case_id, objective_id, scope, phase, revision,
             resource_links_serialization) VALUES (?, ?, ?, ?, ?, ?)""",
            (
                state.case_id, state.objective_id, state.scope, state.phase.value,
                _revision_text(state.revision), _serialize_links(state.resource_links),
            ),
        )
        self._append(transition)
        return True

    def compare_and_swap(self, *, expected_revision, next_state, transition):
        current = self.read(case_id=next_state.case_id)
        if current is None or current.revision != expected_revision:
            return False
        updated = self.connection.execute(
            """UPDATE case_authoritative_states
            SET objective_id=?, scope=?, phase=?, revision=?,
                resource_links_serialization=?
            WHERE case_id=? AND revision=?""",
            (
                next_state.objective_id, next_state.scope, next_state.phase.value,
                _revision_text(next_state.revision),
                _serialize_links(next_state.resource_links),
                next_state.case_id, _revision_text(expected_revision),
            ),
        )
        if updated.rowcount != 1:
            return False
        self.previous = current
        self._append(transition)
        return True


class SqliteCaseLifecycleExecutionStore(SqliteCaseAuthoritativeStateStore):
    """Trusted local execution capability; does not authorize its caller."""

    def _initialize_schema(self):
        super()._initialize_schema()
        connection = self._connect()
        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS case_lifecycle_completions (
                    transition_id TEXT PRIMARY KEY NOT NULL,
                    request_document BLOB NOT NULL,
                    completion_document BLOB NOT NULL,
                    FOREIGN KEY (transition_id)
                        REFERENCES case_lifecycle_transitions(transition_id)
                )
            """)
        finally:
            connection.close()

    @staticmethod
    def _validate_request(request):
        if type(request) not in (CaseOpeningRequest, CaseTransitionRequest):
            raise TypeError("request must be an exact lifecycle request")

    def _recover_on(self, connection, request):
        row = connection.execute(
            """SELECT request_document, completion_document
            FROM case_lifecycle_completions WHERE transition_id=?""",
            (request.transition_id,),
        ).fetchone()
        if row is None:
            return None
        stored_request = deserialize_case_lifecycle(row["request_document"])
        result = deserialize_case_lifecycle(row["completion_document"])
        if type(result) is not CaseLifecycleCompletion:
            raise ValueError("stored completion has an invalid type")
        if stored_request != result.request:
            raise ValueError("stored request and completion disagree")
        return match_case_lifecycle_completion(request=request, completion=result)

    def recover(self, *, request):
        self._validate_request(request)
        connection = self._connect()
        try:
            return self._recover_on(connection, request)
        finally:
            connection.close()

    def execute(self, *, request, write_deadline_ns=None):
        self._validate_request(request)
        request_document = serialize_case_lifecycle(request)
        _check_write_deadline(write_deadline_ns)
        connection = self._connect()
        with WriteTransactionMeasurement(
            operation="case.execute", observer=self._write_observer,
        ) as measurement:
            try:
                if self._write_acquisition is None or write_deadline_ns is None:
                    _configure_write_wait(connection, write_deadline_ns)
                    measurement.begin(connection)
                else:
                    measurement.begin(
                        connection,
                        acquisition=lambda conn: self._write_acquisition.begin(
                            conn, deadline_ns=write_deadline_ns,
                        ),
                    )
                _check_write_deadline(write_deadline_ns)
                existing = self._recover_on(connection, request)
                if existing is not None:
                    measurement.rollback_sql(connection)
                    return existing

                legacy = connection.execute(
                    "SELECT 1 FROM case_lifecycle_transitions WHERE transition_id=?",
                    (request.transition_id,),
                ).fetchone()
                if legacy is not None:
                    raise ValueError(
                        "transition exists without a recoverable original request"
                    )

                view = _TransactionView(self, connection)
                if type(request) is CaseOpeningRequest:
                    state = open_case(
                        store=view, case_id=request.case_id,
                        objective_id=request.objective_id, scope=request.scope,
                        transition_id=request.transition_id,
                        resource_links=request.resource_links,
                    )
                else:
                    state = apply_case_lifecycle_transition(
                        store=view, case_id=request.case_id,
                        expected_revision=request.expected_revision,
                        transition_id=request.transition_id,
                        to_phase=request.to_phase,
                        resource_links=request.resource_links,
                    )
                if state is None:
                    measurement.rollback_sql(connection)
                    return None

                result = CaseLifecycleCompletion(
                    request=request, state=state,
                    transition=view.record, previous_state=view.previous,
                )
                connection.execute(
                    """INSERT INTO case_lifecycle_completions
                    (transition_id, request_document, completion_document)
                    VALUES (?, ?, ?)""",
                    (
                        request.transition_id, request_document,
                        serialize_case_lifecycle(result),
                    ),
                )
                _check_write_deadline(write_deadline_ns)
                measurement.commit_sql(connection)
                return result
            except sqlite3.OperationalError as error:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                code = getattr(error, "sqlite_errorcode", None)
                if (
                    code is not None and (code & 0xff) == sqlite3.SQLITE_BUSY
                    and write_deadline_ns is not None
                    and perf_counter_ns() >= write_deadline_ns
                ):
                    raise CaseWriteDeadlineExceeded(
                        "case_write_deadline_exceeded"
                    ) from error
                raise
            except BaseException:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                raise
            finally:
                connection.close()
