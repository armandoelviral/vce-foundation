from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)


class RecoveryRegistry:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: RecoveryRecord,
    ) -> None:

        self._records[
            record.recovery_id
        ] = record

    def get(
        self,
        recovery_id: str,
    ):

        return self._records.get(
            recovery_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def recovery_ids(
        self,
    ):

        return list(
            self._records.keys()
        )
