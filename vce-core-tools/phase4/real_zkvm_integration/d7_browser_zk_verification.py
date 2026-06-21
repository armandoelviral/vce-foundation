from phase4.real_zkvm_integration.d5_zk_proof_attachment import (
    D5zkProofAttachment,
)


class D7BrowserZkVerification:

    @staticmethod
    def verify(
        attachment: D5zkProofAttachment,
    ) -> bool:

        if not attachment.d5_artifact_id:
            return False

        if not attachment.proof_artifact_id:
            return False

        if not attachment.proof_hash:
            return False

        return True
