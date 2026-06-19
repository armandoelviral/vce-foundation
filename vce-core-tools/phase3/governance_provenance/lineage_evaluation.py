from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)


class LineageEvaluation:

    @staticmethod
    def evaluate(
        record: GovernanceProvenanceRecord,
    ) -> bool:

        if not record.current_snapshot:
            return False

        if not record.previous_snapshot:
            return False

        if (
            record.current_snapshot
            == record.previous_snapshot
        ):
            return False

        return True
