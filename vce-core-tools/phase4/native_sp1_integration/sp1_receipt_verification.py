from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


class SP1ReceiptVerification:

    @staticmethod
    def verify(
        receipt: SP1ReceiptArtifact,
    ) -> bool:

        if not receipt.receipt_id:
            return False

        if not receipt.request_id:
            return False

        if not receipt.proof_hash:
            return False

        if not receipt.verification_key_hash:
            return False

        return True
