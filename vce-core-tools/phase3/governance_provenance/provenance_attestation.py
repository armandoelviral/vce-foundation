from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_provenance.governance_provenance_record import (
    GovernanceProvenanceRecord,
)


class ProvenanceAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        record: GovernanceProvenanceRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_provenance",
            evidence_hash=(
                record.provenance_id
            ),
        )
