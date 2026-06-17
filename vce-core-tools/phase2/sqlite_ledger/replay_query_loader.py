import json
from pathlib import Path

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)


class ReplayQueryLoader:

    def __init__(
        self,
        db_path: Path,
    ):

        self.db_path = Path(
            db_path
        )

    def load(
        self,
    ):

        rows = EventQuery(
            self.db_path
        ).all()

        events = []

        for row in rows:

            events.append(
                {
                    "lsn": row["lsn"],
                    "opcode": row["opcode"],
                    "payload": json.loads(
                        row["payload_json"]
                    ),
                }
            )

        return events
