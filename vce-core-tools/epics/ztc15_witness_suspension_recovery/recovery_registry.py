from typing import List

from epics.ztc15_witness_suspension_recovery.recovery_record import (
    RecoveryRecord,
)


class RecoveryRegistry:

    def __init__(self):

        self._records: List[
            RecoveryRecord
        ] = []

    def add(
        self,
        record: RecoveryRecord,
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

    def is_recovered(
        self,
        witness_id: str,
    ) -> bool:

        return any(
            record.witness_id == witness_id
            for record in self._records
        )
