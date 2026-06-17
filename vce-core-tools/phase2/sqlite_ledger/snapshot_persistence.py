import sqlite3
from pathlib import Path


class SnapshotPersistence:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def initialize(
        self,
    ) -> None:

        connection = sqlite3.connect(
            self.db_path
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY,
                lsn INTEGER NOT NULL,
                state_hash TEXT NOT NULL
            )
            """
        )

        connection.commit()
        connection.close()

    def save(
        self,
        snapshot_id: str,
        lsn: int,
        state_hash: str,
    ) -> None:

        connection = sqlite3.connect(
            self.db_path
        )

        connection.execute(
            """
            INSERT INTO snapshots (
                snapshot_id,
                lsn,
                state_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                snapshot_id,
                lsn,
                state_hash,
            ),
        )

        connection.commit()
        connection.close()

    def latest(
        self,
    ):

        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            """
            SELECT
                snapshot_id,
                lsn,
                state_hash
            FROM snapshots
            ORDER BY lsn DESC
            LIMIT 1
            """
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return dict(row)

    def count(
        self,
    ) -> int:

        connection = sqlite3.connect(
            self.db_path
        )

        cursor = connection.execute(
            "SELECT COUNT(*) FROM snapshots"
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count
