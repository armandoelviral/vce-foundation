from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)


class SignatureEvaluation:

    @staticmethod
    def evaluate(
        signature: HybridSignatureRecord,
    ) -> bool:

        if not signature.witness_did:
            return False

        if not signature.classical_signature:
            return False

        if not signature.pqc_signature:
            return False

        return True
