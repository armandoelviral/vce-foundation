from pathlib import Path

from phase2.persistent_wal.wal_read_engine import (
    WALReadEngine,
)


class WALReplayLoader:

    def __init__(
        self,
        wal_path: Path,
    ):

        self.reader = WALReadEngine(
            wal_path=wal_path,
        )

    def load(
        self,
    ):

        records = self.reader.read_all()

        events = []

        for record in records:

            events.append(
                {
                    "lsn": record.lsn,
                    "opcode": record.opcode,
                    "payload": record.payload,
                }
            )

        return events
