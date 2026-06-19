from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)


class SignatureAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        signature: HybridSignatureRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="hybrid_signature",
            evidence_hash=(
                signature.witness_did
            ),
        )
