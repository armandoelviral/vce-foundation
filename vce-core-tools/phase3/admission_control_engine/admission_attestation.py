from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)


class AdmissionAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        decision: AdmissionDecision,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="admission_decision",
            evidence_hash=decision.status,
        )
