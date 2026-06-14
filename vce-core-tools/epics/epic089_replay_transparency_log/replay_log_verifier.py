from typing import List

from epics.epic089_replay_transparency_log.replay_log_record import (
    ReplayLogRecord,
)


class ReplayLogVerifier:

    @staticmethod
    def verify(
        records: List[ReplayLogRecord],
    ) -> bool:

        if not records:
            return True

        if records[0].previous_hash != "GENESIS":
            return False

        for index in range(1, len(records)):

            previous = records[index - 1]
            current = records[index]

            if current.previous_hash != previous.current_hash:
                return False

        return True
