from phase3.governance_escalation.escalation_record import (
    EscalationRecord,
)


class SuspensionEvaluation:

    @staticmethod
    def evaluate(
        record: EscalationRecord,
    ) -> bool:

        return (
            record.severity
            == "HIGH"
        )
