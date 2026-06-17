import hashlib
import json
from pathlib import Path

from phase2.sqlite_ledger.event_insert import (
    EventInsert,
)

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)


class SQLiteAppendEngine:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def append(
        self,
        lsn: int,
        opcode: str,
        payload: dict,
    ):

        previous_hash = self._last_hash()

        payload_json = json.dumps(
            payload,
            sort_keys=True,
        )

        current_hash = self._compute_hash(
            lsn=lsn,
            opcode=opcode,
            payload_json=payload_json,
            previous_hash=previous_hash,
        )

        EventInsert(
            self.db_path
        ).insert(
            lsn=lsn,
            opcode=opcode,
            payload_json=payload_json,
            previous_hash=previous_hash,
            current_hash=current_hash,
        )

        return {
            "lsn": lsn,
            "opcode": opcode,
            "payload_json": payload_json,
            "previous_hash": previous_hash,
            "current_hash": current_hash,
        }

    def _last_hash(
        self,
    ) -> str:

        rows = EventQuery(
            self.db_path
        ).all()

        if not rows:
            return "GENESIS"

        return rows[-1]["current_hash"]

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
