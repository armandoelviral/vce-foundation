import sqlite3
from pathlib import Path


class EventQuery:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def all(
        self,
    ):

        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = (
            sqlite3.Row
        )

        cursor = connection.execute(
            """
            SELECT
                lsn,
                opcode,
                payload_json,
                previous_hash,
                current_hash
            FROM wal_records
            ORDER BY lsn
            """
        )

        rows = [
            dict(row)
            for row in cursor.fetchall()
        ]

        connection.close()

        return rows
