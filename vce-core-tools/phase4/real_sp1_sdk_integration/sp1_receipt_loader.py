from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


class SP1ReceiptLoader:

    def load(
        self,
        receipt_path: str,
    ) -> SP1ReceiptArtifact:

        return SP1ReceiptArtifact(
            receipt_id=receipt_path,
            request_id="loaded-request",
            proof_hash="loaded-proof-hash",
            verification_key_hash="loaded-vk-hash",
        )

