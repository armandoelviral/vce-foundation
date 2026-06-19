from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)


class RootAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        root: GovernanceMerkleRootRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_merkle_root",
            evidence_hash=root.root_id,
        )
