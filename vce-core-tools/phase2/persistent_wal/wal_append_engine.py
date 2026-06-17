import hashlib
import json
from pathlib import Path

from phase2.persistent_wal.wal_schema import (
    WALRecord,
)


class WALAppendEngine:

    def __init__(
        self,
        wal_path: Path,
    ):

        self.wal_path = Path(
            wal_path
        )

    def append(
        self,
        lsn: int,
        opcode: str,
        payload: dict,
    ) -> WALRecord:

        previous_hash = self._last_hash()

        current_hash = self._compute_hash(
            lsn=lsn,
            opcode=opcode,
            payload=payload,
            previous_hash=previous_hash,
        )

        record = WALRecord(
            lsn=lsn,
            opcode=opcode,
            payload=payload,
            previous_hash=previous_hash,
            current_hash=current_hash,
        )

        self.wal_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.wal_path.open(
            "a",
            encoding="utf-8",
        ) as handle:

            handle.write(
                json.dumps(
                    record.to_dict(),
                    sort_keys=True,
                )
            )

            handle.write(
                "\n"
            )

        return record

    def _last_hash(
        self,
    ) -> str:

        if not self.wal_path.exists():
            return "GENESIS"

        lines = self.wal_path.read_text(
            encoding="utf-8",
        ).splitlines()

        if not lines:
            return "GENESIS"

        last_record = json.loads(
            lines[-1]
        )

        return last_record[
            "current_hash"
        ]

    def _compute_hash(
        self,
        lsn: int,
        opcode: str,
        payload: dict,
        previous_hash: str,
    ) -> str:

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
