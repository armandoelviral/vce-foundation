from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)


class ExecutionAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        request: ExecutionRequestRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_execution",
            evidence_hash=request.request_id,
        )
