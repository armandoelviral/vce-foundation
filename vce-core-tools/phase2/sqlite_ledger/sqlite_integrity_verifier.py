import hashlib
import json
from pathlib import Path

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)


class SQLiteIntegrityVerifier:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def verify(
        self,
    ) -> bool:

        rows = EventQuery(
            self.db_path
        ).all()

        expected_previous = "GENESIS"

        for row in rows:

            if (
                row["previous_hash"]
                != expected_previous
            ):
                return False

            computed_hash = self._compute_hash(
                lsn=row["lsn"],
                opcode=row["opcode"],
                payload_json=row["payload_json"],
                previous_hash=row[
                    "previous_hash"
                ],
            )

            if (
                computed_hash
                != row["current_hash"]
            ):
                return False

            expected_previous = row[
                "current_hash"
            ]

        return True

    def _compute_hash(
        self,
        lsn: int,
        opcode: str,
        payload_json: str,
        previous_hash: str,
    ) -> str:

        material = {
            "lsn": lsn,
            "opcode": opcode,
            "payload_json": payload_json,
            "previous_hash": previous_hash,
        }

        return hashlib.sha256(
            json.dumps(
                material,
                sort_keys=True,
            ).encode(
                "utf-8"
            )
        ).hexdigest()
