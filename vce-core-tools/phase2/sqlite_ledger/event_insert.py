import sqlite3
from pathlib import Path


class EventInsert:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def insert(
        self,
        lsn: int,
        opcode: str,
        payload_json: str,
        previous_hash: str,
        current_hash: str,
    ) -> None:

        connection = sqlite3.connect(
            self.db_path
        )

        connection.execute(
            """
            INSERT INTO wal_records (
                lsn,
                opcode,
                payload_json,
                previous_hash,
                current_hash
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                lsn,
                opcode,
                payload_json,
                previous_hash,
                current_hash,
            ),
        )

        connection.commit()
        connection.close()
