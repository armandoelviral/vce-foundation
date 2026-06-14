import hashlib
import json

from epics.epic089_replay_transparency_log.replay_log_record import (
    ReplayLogRecord,
)

from epics.epic089_replay_transparency_log.replay_transparency_entry import (
    ReplayTransparencyEntry,
)


class ReplayTransparencyLog:

    def __init__(self):
        self.records = []

    def append(
        self,
        entry: ReplayTransparencyEntry,
    ) -> ReplayLogRecord:

        sequence = len(self.records) + 1

        previous_hash = (
            "GENESIS"
            if not self.records
            else self.records[-1].current_hash
        )

        payload = {
            "sequence": sequence,
            "previous_hash": previous_hash,
            "entry": entry.to_dict(),
        }

        current_hash = hashlib.sha256(
            json.dumps(
                payload,
                sort_keys=True,
            ).encode()
        ).hexdigest()

        record = ReplayLogRecord(
            sequence=sequence,
            previous_hash=previous_hash,
            current_hash=current_hash,
            replay_id=entry.replay_id,
        )

        self.records.append(record)

        return record
