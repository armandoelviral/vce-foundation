from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)


class RecoveryEvaluation:

    RECOVERABLE_REASONS = {
        "manual_remediation",
        "automatic_recovery",
    }

    @staticmethod
    def evaluate(
        record: RecoveryRecord,
    ) -> bool:

        return (
            record.recovery_reason
            in RecoveryEvaluation.RECOVERABLE_REASONS
        )
