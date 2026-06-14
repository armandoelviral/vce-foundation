from typing import List

from epics.ztc15_witness_suspension_recovery.witness_suspension_record import (
    WitnessSuspensionRecord,
)


class SuspensionRegistry:

    def __init__(self):

        self._records: List[
            WitnessSuspensionRecord
        ] = []

    def add(
        self,
        record: WitnessSuspensionRecord,
    ) -> None:

        self._records.append(
            record
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def is_suspended(
        self,
        witness_id: str,
    ) -> bool:

        return any(
            record.witness_id == witness_id
            for record in self._records
        )
