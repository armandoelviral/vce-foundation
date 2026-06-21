from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)


class D7RealBrowserVerification:

    @staticmethod
    def verify(
        attachment: D5RealProofAttachment,
    ) -> bool:

        if not attachment.d5_artifact_id:
            return False

        if not attachment.receipt_id:
            return False

        if not attachment.proof_hash:
            return False

        if not attachment.verification_key_hash:
            return False

        return True
