from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)


class EnforcementAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        decision: EnforcementDecision,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="enforcement_decision",
            evidence_hash=decision.status,
        )
