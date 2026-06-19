from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.trust_policy_engine.trust_decision import (
    TrustDecision,
)


class TrustAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        decision: TrustDecision,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="trust_decision",
            evidence_hash=decision.status,
        )
