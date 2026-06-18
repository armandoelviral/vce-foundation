from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)


class ExecutionAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        execution: ExecutionRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="execution",
            evidence_hash=execution.execution_id,
        )
