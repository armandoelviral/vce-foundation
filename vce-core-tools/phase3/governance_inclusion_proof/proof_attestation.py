from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)


class ProofAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        proof: InclusionProofRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="governance_inclusion_proof",
            evidence_hash=proof.proof_hash,
        )
