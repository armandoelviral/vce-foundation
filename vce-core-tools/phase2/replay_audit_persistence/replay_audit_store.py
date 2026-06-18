from phase2.replay_audit_persistence.replay_audit_record import (
    ReplayAuditRecord,
)


class ReplayAuditStore:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: ReplayAuditRecord,
    ) -> None:

        self._records[
            record.replay_id
        ] = record

    def get(
        self,
        replay_id: str,
    ):

        return self._records.get(
            replay_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
