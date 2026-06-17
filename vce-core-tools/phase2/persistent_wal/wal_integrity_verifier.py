import hashlib
import json
from pathlib import Path


class WALIntegrityVerifier:

    def __init__(
        self,
        wal_path: Path,
    ):

        self.wal_path = Path(
            wal_path
        )

    def verify(
        self,
    ) -> bool:

        if not self.wal_path.exists():
            return True

        records = []

        for line in self.wal_path.read_text(
            encoding="utf-8"
        ).splitlines():

            records.append(
                json.loads(
                    line
                )
            )

        expected_previous = "GENESIS"

        for record in records:

            if (
                record["previous_hash"]
                != expected_previous
            ):
                return False

            computed_hash = (
                self._compute_hash(
                    lsn=record["lsn"],
                    opcode=record["opcode"],
                    payload=record["payload"],
                    previous_hash=record[
                        "previous_hash"
                    ],
                )
            )

            if (
                computed_hash
                != record["current_hash"]
            ):
                return False

            expected_previous = record[
                "current_hash"
            ]

        return True

    def _compute_hash(
        self,
        lsn,
        opcode,
        payload,
        previous_hash,
    ):

        material = {
            "lsn": lsn,
            "opcode": opcode,
            "payload": payload,
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
