from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)


class GovernanceMerkleAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        leaf: GovernanceMerkleLeaf,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_merkle_leaf",
            evidence_hash=(
                leaf.leaf_id
            ),
        )
