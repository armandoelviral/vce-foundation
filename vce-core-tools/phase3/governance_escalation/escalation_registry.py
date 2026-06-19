from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)


class EscalationRegistry:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: EscalationRecord,
    ) -> None:

        self._records[
            record.escalation_id
        ] = record

    def get(
        self,
        escalation_id: str,
    ):

        return self._records.get(
            escalation_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
