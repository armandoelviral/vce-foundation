import json
import sqlite3
from dataclasses import asdict, replace
from pathlib import Path

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import (
    RetailEvaluatorBindingChange,
)


class RetailEvaluatorBindingConflict(ValueError):
    """Conflicting event, revision or binding transition."""


def _document(change):
    return json.dumps(
        asdict(change), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def _decode(document):
    value = json.loads(document)
    raw = value["snapshot"]["binding"]
    actor = raw["actor"]
    binding = RetailEvaluatorBinding(
        binding_id=raw["binding_id"], revision=raw["revision"],
        principal=AuthenticatedPrincipal(**raw["principal"]),
        actor=RetailProcessActor(
            actor_id=actor["actor_id"], customer_id=actor["customer_id"],
            actor_type=ActorType(actor["actor_type"]),
            organization_id=actor["organization_id"],
            role=RetailProcessRole(**actor["role"]),
        ),
        case_id=raw["case_id"],
        valid_from=raw["valid_from"], expires_at=raw["expires_at"],
    )
    change = RetailEvaluatorBindingChange(
        event_id=value["event_id"],
        snapshot=RetailEvaluatorBindingSnapshot(
            binding, value["snapshot"]["revoked"],
        ),
        administrator=AuthenticatedPrincipal(**value["administrator"]),
        recorded_at=value["recorded_at"],
    )
    if _document(change) != document:
        raise ValueError("stored binding change is not canonical")
    return change


def _require_successor(previous, current):
    binding = current.binding
    if previous is None:
        if binding.revision != 1 or current.revoked:
            raise RetailEvaluatorBindingConflict(
                "first revision must be active revision 1"
            )
        return

    old = previous.binding
    if previous.revoked:
        raise RetailEvaluatorBindingConflict("revoked binding is terminal")
    if binding.revision != old.revision + 1:
        raise RetailEvaluatorBindingConflict("revision must be the next revision")
    if (
        binding.binding_id != old.binding_id
        or binding.principal != old.principal
        or binding.actor != old.actor
        or binding.case_id != old.case_id
    ):
        raise RetailEvaluatorBindingConflict("binding association cannot change")
    if current.revoked and binding != replace(old, revision=old.revision + 1):
        raise RetailEvaluatorBindingConflict(
            "revocation must preserve the previous binding content"
        )


class SqliteRetailEvaluatorBindings:
    """Trusted append-only storage, not an administrative authorization gate."""

    def __init__(self, *, database_path: str | Path) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or Path")
        if not str(database_path).strip() or str(database_path) == ":memory:":
            raise ValueError("database_path must identify a file")
        self._path = str(database_path)
        connection = self._connect()
        try:
            mode = connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if mode.lower() != "wal":
                raise RuntimeError("WAL mode was not established")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS retail_evaluator_binding_history (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL UNIQUE,
                    binding_id TEXT NOT NULL,
                    revision TEXT NOT NULL,
                    document TEXT NOT NULL,
                    UNIQUE(binding_id, revision)
                )
            """)
        finally:
            connection.close()

    def _connect(self):
        connection = sqlite3.connect(
            self._path, timeout=5, isolation_level=None,
        )
        try:
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    def _history(self, connection, binding_id):
        rows = connection.execute(
            """
            SELECT event_id, revision, document
            FROM retail_evaluator_binding_history
            WHERE binding_id=? ORDER BY sequence
            """,
            (binding_id,),
        ).fetchall()
        history = []
        previous = None
        for event_id, revision, document in rows:
            change = _decode(document)
            binding = change.snapshot.binding
            if (
                change.event_id != event_id
                or binding.binding_id != binding_id
                or str(binding.revision) != revision
            ):
                raise ValueError("stored binding metadata mismatch")
            _require_successor(previous, change.snapshot)
            history.append(change)
            previous = change.snapshot
        return tuple(history)

    def apply(self, *, change: RetailEvaluatorBindingChange) -> bool:
        if not isinstance(change, RetailEvaluatorBindingChange):
            raise TypeError("change must be a RetailEvaluatorBindingChange")
        document = _document(change)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT document FROM retail_evaluator_binding_history "
                "WHERE event_id=?",
                (change.event_id,),
            ).fetchone()
            if existing is not None:
                _decode(existing[0])
                if existing[0] != document:
                    raise RetailEvaluatorBindingConflict("event identity conflict")
                self._history(connection, change.snapshot.binding.binding_id)
                connection.execute("COMMIT")
                return True

            binding = change.snapshot.binding
            history = self._history(connection, binding.binding_id)
            previous = history[-1].snapshot if history else None
            _require_successor(previous, change.snapshot)
            connection.execute(
                """
                INSERT INTO retail_evaluator_binding_history
                (event_id, binding_id, revision, document)
                VALUES (?, ?, ?, ?)
                """,
                (change.event_id, binding.binding_id,
                 str(binding.revision), document),
            )
            connection.execute("COMMIT")
            return True
        except BaseException as error:
            if connection.in_transaction:
                try:
                    connection.execute("ROLLBACK")
                except BaseException as rollback_error:
                    error.add_note(
                        "Rollback also failed: "
                        + type(rollback_error).__name__
                    )
            raise
        finally:
            connection.close()

    def read_history(self, *, binding_id: str):
        if not isinstance(binding_id, str):
            raise TypeError("binding_id must be a string")
        if not binding_id.strip():
            raise ValueError("binding_id must not be empty")
        connection = self._connect()
        try:
            return self._history(connection, binding_id)
        finally:
            connection.close()

    def read_snapshot_in_transaction(
        self, *, connection: sqlite3.Connection, binding_id: str,
    ):
        """Read through the caller-owned transaction without ending it.

        The supplied connection selects the database and snapshot.
        The caller is responsible for using the admission database.
        """
        if not isinstance(connection, sqlite3.Connection):
            raise TypeError("connection must be a SQLite connection")
        if not isinstance(binding_id, str):
            raise TypeError("binding_id must be a string")
        if not binding_id.strip():
            raise ValueError("binding_id must not be empty")
        if not connection.in_transaction:
            raise ValueError("an active transaction is required")
        history = self._history(connection, binding_id)
        return history[-1].snapshot if history else None

    def read_snapshot(self, *, binding_id: str):
        history = self.read_history(binding_id=binding_id)
        return history[-1].snapshot if history else None
