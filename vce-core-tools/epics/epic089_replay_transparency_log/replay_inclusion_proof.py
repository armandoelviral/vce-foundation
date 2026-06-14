from typing import Dict
from typing import List

from epics.epic089_replay_transparency_log.replay_log_record import (
    ReplayLogRecord,
)


class ReplayInclusionProof:

    @staticmethod
    def build(
        records: List[ReplayLogRecord],
        replay_id: str,
    ) -> Dict:

        for record in records:

            if record.replay_id == replay_id:
                return {
                    "included": True,
                    "sequence": record.sequence,
                    "current_hash": record.current_hash,
                }

        return {
            "included": False,
        }
