from sp001.infrastructure.write_transaction_measurement import (
    WriteTransactionMeasurement,
)
import json
import sqlite3
from time import perf_counter_ns
from pathlib import Path

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_authoritative_state_store import (
    CaseAuthoritativeStateStore,
    CaseWriteDeadlineExceeded,
)
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink


_REVISION_WIDTH = 20
_STATE_TABLE = "case_authoritative_states"
_TRANSITION_TABLE = "case_lifecycle_transitions"
_PHASE_VALUES = tuple(phase.value for phase in CaseLifecyclePhase)
_PHASE_SQL = ", ".join(f"'{value}'" for value in _PHASE_VALUES)


def _revision_text(revision: int) -> str:
    if isinstance(revision, bool) or not isinstance(revision, int):
        raise TypeError("revision must be an integer")
    if revision < 1 or revision > (1 << 64) - 1:
        raise ValueError("revision must be a positive uint64")
    return f"{revision:0{_REVISION_WIDTH}d}"


def _serialize_links(links: tuple[CaseResourceLink, ...]) -> str:
    return json.dumps(
        [
            {
                "relationship": link.relationship,
                "resource_id": link.resource_id,
                "resource_type": link.resource_type,
            }
            for link in links
        ],
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )


def _deserialize_links(serialization: str) -> tuple[CaseResourceLink, ...]:
    try:
        value = json.loads(serialization)
    except (TypeError, json.JSONDecodeError) as error:
        raise ValueError("stored resource links are invalid JSON") from error
    if not isinstance(value, list):
        raise ValueError("stored resource links must be a JSON array")

    links = []
    for item in value:
        if not isinstance(item, dict) or set(item) != {
            "relationship",
            "resource_id",
            "resource_type",
        }:
            raise ValueError("stored resource link has invalid fields")
        links.append(
            CaseResourceLink(
                relationship=item["relationship"],
                resource_type=item["resource_type"],
                resource_id=item["resource_id"],
            )
        )

    result = tuple(links)
    if _serialize_links(result) != serialization:
        raise ValueError("stored resource links are not canonical")
    return result


def _validate_pair(
    *,
    state: CaseAuthoritativeState,
    transition: CaseLifecycleTransitionRecord,
    expected_revision: int | None,
    from_phase: CaseLifecyclePhase | None,
) -> None:
    if not isinstance(state, CaseAuthoritativeState):
        raise TypeError("state must be a CaseAuthoritativeState")
    if not isinstance(transition, CaseLifecycleTransitionRecord):
        raise TypeError(
            "transition must be a CaseLifecycleTransitionRecord"
        )
    if transition.case_id != state.case_id:
        raise ValueError("transition and state must use the same case_id")
    if transition.to_phase is not state.phase:
        raise ValueError("transition target must match state phase")
    if transition.resource_links != state.resource_links:
        raise ValueError("transition links must match state links")

    if expected_revision is None:
        if state.revision != 1 or transition.revision != 1:
            raise ValueError("created case must start at revision one")
        if transition.from_phase is not None:
            raise ValueError("initial transition must not have a from_phase")
        return

    successor = expected_revision + 1
    if state.revision != successor or transition.revision != successor:
        raise ValueError("next revision must be the exact successor")
    if transition.from_phase is not from_phase:
        raise ValueError("transition source must match current phase")


def _check_write_deadline(deadline_ns):
    if deadline_ns is None:
        return
    if type(deadline_ns) is not int:
        raise TypeError("write_deadline_ns must be an integer")
    if deadline_ns < 0:
        raise ValueError("write_deadline_ns must be nonnegative")
    if perf_counter_ns() >= deadline_ns:
        raise CaseWriteDeadlineExceeded("case_write_deadline_exceeded")


def _configure_write_wait(connection, deadline_ns):
    if deadline_ns is None:
        return
    _check_write_deadline(deadline_ns)
    remaining_ns = deadline_ns - perf_counter_ns()
    if remaining_ns <= 0:
        raise CaseWriteDeadlineExceeded("case_write_deadline_exceeded")
    current_ms = connection.execute("PRAGMA busy_timeout").fetchone()[0]
    # Round up to the next millisecond; preserve any stricter connection limit.
    remaining_ms = (remaining_ns + 999_999) // 1_000_000
    wait_ms = min(current_ms, remaining_ms)
    connection.execute(f"PRAGMA busy_timeout={wait_ms}")


class SqliteCaseAuthoritativeStateStore(CaseAuthoritativeStateStore):
    """Persist current case state and its append-only transition history."""

    __slots__ = ("_database_path", "_write_observer")

    def __init__(self, *, database_path: str | Path, write_observer=None) -> None:
        if write_observer is not None and not callable(write_observer):
            raise TypeError("write_observer must be callable")
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or pathlib.Path")
        if isinstance(database_path, str) and not database_path.strip():
            raise ValueError("database_path must not be empty")

        self._write_observer = write_observer
        self._database_path = str(database_path)
        self._initialize_schema()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self._database_path,
            timeout=5.0,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize_schema(self) -> None:
        connection = self._connect()
        try:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {_STATE_TABLE} (
                    case_id TEXT PRIMARY KEY NOT NULL,
                    objective_id TEXT NOT NULL,
                    scope TEXT NOT NULL,
                    phase TEXT NOT NULL
                        CHECK (phase IN ({_PHASE_SQL})),
                    revision TEXT NOT NULL
                        CHECK (
                            length(revision) = {_REVISION_WIDTH}
                            AND revision NOT GLOB '*[^0-9]*'
                        ),
                    resource_links_serialization TEXT NOT NULL
                )
                """
            )
            connection.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {_TRANSITION_TABLE} (
                    case_id TEXT NOT NULL,
                    revision TEXT NOT NULL
                        CHECK (
                            length(revision) = {_REVISION_WIDTH}
                            AND revision NOT GLOB '*[^0-9]*'
                        ),
                    transition_id TEXT NOT NULL UNIQUE,
                    from_phase TEXT
                        CHECK (
                            from_phase IS NULL
                            OR from_phase IN ({_PHASE_SQL})
                        ),
                    to_phase TEXT NOT NULL
                        CHECK (to_phase IN ({_PHASE_SQL})),
                    resource_links_serialization TEXT NOT NULL,
                    PRIMARY KEY (case_id, revision),
                    FOREIGN KEY (case_id)
                        REFERENCES {_STATE_TABLE}(case_id)
                )
                """
            )
        finally:
            connection.close()

    @staticmethod
    def _state_from_row(row: sqlite3.Row) -> CaseAuthoritativeState:
        try:
            phase = CaseLifecyclePhase(row["phase"])
            revision_text = row["revision"]
            revision = int(revision_text)
            if _revision_text(revision) != revision_text:
                raise ValueError("stored revision is not canonical")
            links = _deserialize_links(
                row["resource_links_serialization"]
            )
            return CaseAuthoritativeState(
                case_id=row["case_id"],
                objective_id=row["objective_id"],
                scope=row["scope"],
                phase=phase,
                revision=revision,
                resource_links=links,
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("stored case state is invalid") from error

    @staticmethod
    def _transition_from_row(
        row: sqlite3.Row,
    ) -> CaseLifecycleTransitionRecord:
        try:
            revision_text = row["revision"]
            revision = int(revision_text)
            if _revision_text(revision) != revision_text:
                raise ValueError("stored revision is not canonical")
            from_value = row["from_phase"]
            return CaseLifecycleTransitionRecord(
                case_id=row["case_id"],
                transition_id=row["transition_id"],
                revision=revision,
                from_phase=(
                    None
                    if from_value is None
                    else CaseLifecyclePhase(from_value)
                ),
                to_phase=CaseLifecyclePhase(row["to_phase"]),
                resource_links=_deserialize_links(
                    row["resource_links_serialization"]
                ),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("stored case transition is invalid") from error

    def read(
        self,
        *,
        case_id: str,
    ) -> CaseAuthoritativeState | None:
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("case_id must be a non-empty string")

        connection = self._connect()
        try:
            row = connection.execute(
                f"SELECT * FROM {_STATE_TABLE} WHERE case_id = ?",
                (case_id,),
            ).fetchone()
            return None if row is None else self._state_from_row(row)
        finally:
            connection.close()

    def read_transitions(
        self,
        *,
        case_id: str,
    ) -> tuple[CaseLifecycleTransitionRecord, ...]:
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("case_id must be a non-empty string")

        connection = self._connect()
        try:
            rows = connection.execute(
                f"""
                SELECT * FROM {_TRANSITION_TABLE}
                WHERE case_id = ?
                ORDER BY revision
                """,
                (case_id,),
            ).fetchall()
            return tuple(self._transition_from_row(row) for row in rows)
        finally:
            connection.close()

    def create(
        self,
        *,
        state: CaseAuthoritativeState,
        transition: CaseLifecycleTransitionRecord,
        write_deadline_ns: int | None = None,
    ) -> bool:
        _validate_pair(
            state=state,
            transition=transition,
            expected_revision=None,
            from_phase=None,
        )
        _check_write_deadline(write_deadline_ns)
        connection = self._connect()
        with WriteTransactionMeasurement(
            operation="case.create", observer=self._write_observer,
        ) as measurement:
            try:
                _configure_write_wait(connection, write_deadline_ns)
                measurement.begin(connection)
                _check_write_deadline(write_deadline_ns)
                connection.execute(
                    f"""
                    INSERT INTO {_STATE_TABLE} (
                        case_id, objective_id, scope, phase, revision,
                        resource_links_serialization
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        state.case_id,
                        state.objective_id,
                        state.scope,
                        state.phase.value,
                        _revision_text(state.revision),
                        _serialize_links(state.resource_links),
                    ),
                )
                connection.execute(
                    f"""
                    INSERT INTO {_TRANSITION_TABLE} (
                        case_id, revision, transition_id, from_phase,
                        to_phase, resource_links_serialization
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        transition.case_id,
                        _revision_text(transition.revision),
                        transition.transition_id,
                        None,
                        transition.to_phase.value,
                        _serialize_links(transition.resource_links),
                    ),
                )
                _check_write_deadline(write_deadline_ns)
                measurement.commit_sql(connection)
                return True
            except sqlite3.IntegrityError:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                return False
            except sqlite3.OperationalError as error:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                code = getattr(error, "sqlite_errorcode", None)
                if (
                    code is not None
                    and code & 0xff == sqlite3.SQLITE_BUSY
                    and write_deadline_ns is not None
                    and perf_counter_ns() >= write_deadline_ns
                ):
                    raise CaseWriteDeadlineExceeded(
                        "case_write_deadline_exceeded"
                    ) from error
                raise
            except Exception:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                raise
            finally:
                connection.close()

    def compare_and_swap(
        self,
        *,
        expected_revision: int,
        next_state: CaseAuthoritativeState,
        transition: CaseLifecycleTransitionRecord,
        write_deadline_ns: int | None = None,
    ) -> bool:
        expected_text = _revision_text(expected_revision)
        _revision_text(expected_revision + 1)

        if not isinstance(next_state, CaseAuthoritativeState):
            raise TypeError("next_state must be a CaseAuthoritativeState")
        if not isinstance(transition, CaseLifecycleTransitionRecord):
            raise TypeError(
                "transition must be a CaseLifecycleTransitionRecord"
            )

        _check_write_deadline(write_deadline_ns)
        connection = self._connect()
        with WriteTransactionMeasurement(
            operation="case.compare_and_swap", observer=self._write_observer,
        ) as measurement:
            try:
                _configure_write_wait(connection, write_deadline_ns)
                measurement.begin(connection)
                _check_write_deadline(write_deadline_ns)
                row = connection.execute(
                    f"SELECT * FROM {_STATE_TABLE} WHERE case_id = ?",
                    (next_state.case_id,),
                ).fetchone()
                if row is None:
                    measurement.rollback_sql(connection)
                    return False

                current = self._state_from_row(row)
                if current.revision != expected_revision:
                    measurement.rollback_sql(connection)
                    return False

                _validate_pair(
                    state=next_state,
                    transition=transition,
                    expected_revision=expected_revision,
                    from_phase=current.phase,
                )

                updated = connection.execute(
                    f"""
                    UPDATE {_STATE_TABLE}
                    SET objective_id = ?, scope = ?, phase = ?, revision = ?,
                        resource_links_serialization = ?
                    WHERE case_id = ? AND revision = ?
                    """,
                    (
                        next_state.objective_id,
                        next_state.scope,
                        next_state.phase.value,
                        _revision_text(next_state.revision),
                        _serialize_links(next_state.resource_links),
                        next_state.case_id,
                        expected_text,
                    ),
                )
                if updated.rowcount != 1:
                    measurement.rollback_sql(connection)
                    return False

                connection.execute(
                    f"""
                    INSERT INTO {_TRANSITION_TABLE} (
                        case_id, revision, transition_id, from_phase,
                        to_phase, resource_links_serialization
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        transition.case_id,
                        _revision_text(transition.revision),
                        transition.transition_id,
                        transition.from_phase.value,
                        transition.to_phase.value,
                        _serialize_links(transition.resource_links),
                    ),
                )
                _check_write_deadline(write_deadline_ns)
                measurement.commit_sql(connection)
                return True
            except sqlite3.IntegrityError:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                return False
            except sqlite3.OperationalError as error:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                code = getattr(error, "sqlite_errorcode", None)
                if (
                    code is not None
                    and code & 0xff == sqlite3.SQLITE_BUSY
                    and write_deadline_ns is not None
                    and perf_counter_ns() >= write_deadline_ns
                ):
                    raise CaseWriteDeadlineExceeded(
                        "case_write_deadline_exceeded"
                    ) from error
                raise
            except Exception:
                if connection.in_transaction:
                    measurement.rollback_sql(connection)
                raise
            finally:
                connection.close()
