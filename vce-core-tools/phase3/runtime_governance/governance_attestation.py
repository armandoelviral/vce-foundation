from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)


class GovernanceAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        decision: GovernanceDecision,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_decision",
            evidence_hash=decision.status,
        )
