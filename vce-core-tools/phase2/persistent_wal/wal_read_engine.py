import json
from pathlib import Path

from phase2.persistent_wal.wal_schema import (
    WALRecord,
)


class WALReadEngine:

    def __init__(
        self,
        wal_path: Path,
    ):

        self.wal_path = Path(
            wal_path
        )

    def read_all(
        self,
    ):

        if not self.wal_path.exists():
            return []

        records = []

        for line in self.wal_path.read_text(
            encoding="utf-8"
        ).splitlines():

            payload = json.loads(
                line
            )

            records.append(
                WALRecord(
                    lsn=payload["lsn"],
                    opcode=payload["opcode"],
                    payload=payload["payload"],
                    previous_hash=payload[
                        "previous_hash"
                    ],
                    current_hash=payload[
                        "current_hash"
                    ],
                )
            )

        return records
