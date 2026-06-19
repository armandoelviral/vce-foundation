from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.multi_party_governance.governance_resolution import (
    GovernanceResolution,
)


class GovernanceAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        resolution: GovernanceResolution,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_resolution",
            evidence_hash=resolution.status,
        )
