import sqlite3
from pathlib import Path


class SQLiteLedgerSchema:

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

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(
            self.db_path
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS wal_records (
                lsn INTEGER PRIMARY KEY,
                opcode TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                current_hash TEXT NOT NULL
            )
            """
        )

        connection.commit()
        connection.close()
