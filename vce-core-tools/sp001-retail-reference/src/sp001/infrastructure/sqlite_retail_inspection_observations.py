import sqlite3
from pathlib import Path

from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict,
    RetailInspectionObservationIdentity,
    StoredRetailInspectionObservation,
)


class SqliteRetailInspectionObservationStore:
    """Append-only exact documents; no authorization or schema validation.

    Versions are independent positive keys. No current-version selection
    or succession policy is imposed. SQLite storage is not an external
    integrity guarantee against privileged database rewriting.
    """

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
                CREATE TABLE IF NOT EXISTS retail_inspection_observations (
                    observation_id TEXT NOT NULL,
                    observation_version TEXT NOT NULL,
                    document TEXT NOT NULL,
                    PRIMARY KEY (observation_id, observation_version)
                )
            """)
        finally:
            connection.close()

    def _connect(self):
        connection = sqlite3.connect(
            self._path, timeout=5.0, isolation_level=None,
        )
        try:
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    def put(
        self, *, observation: StoredRetailInspectionObservation,
    ) -> StoredRetailInspectionObservation:
        if not isinstance(observation, StoredRetailInspectionObservation):
            raise TypeError("observation must be a stored observation")
        identity = observation.identity
        key = (identity.observation_id, str(identity.observation_version))
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""
                INSERT INTO retail_inspection_observations
                    (observation_id, observation_version, document)
                VALUES (?, ?, ?)
                ON CONFLICT(observation_id, observation_version) DO NOTHING
            """, (*key, observation.document))
            row = connection.execute("""
                SELECT document FROM retail_inspection_observations
                WHERE observation_id=? AND observation_version=?
            """, key).fetchone()
            if row is None:
                raise RuntimeError("inserted or existing observation not found")
            if row[0] != observation.document:
                raise RetailInspectionObservationConflict(
                    "observation identity/version has a different document"
                )
            confirmed = StoredRetailInspectionObservation(identity, row[0])
            connection.execute("COMMIT")
            return confirmed
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

    def get(
        self, *, identity: RetailInspectionObservationIdentity,
    ) -> StoredRetailInspectionObservation | None:
        if not isinstance(identity, RetailInspectionObservationIdentity):
            raise TypeError("identity must be an observation identity")
        connection = self._connect()
        try:
            row = connection.execute("""
                SELECT document FROM retail_inspection_observations
                WHERE observation_id=? AND observation_version=?
            """, (
                identity.observation_id, str(identity.observation_version),
            )).fetchone()
            if row is None:
                return None
            return StoredRetailInspectionObservation(identity, row[0])
        finally:
            connection.close()
