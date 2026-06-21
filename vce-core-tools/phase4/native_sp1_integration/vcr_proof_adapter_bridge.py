from phase4.native_sp1_integration.sp1_proof_request import (
    SP1ProofRequest,
)

from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


class VCRProofAdapterBridge:

    def submit(
        self,
        request: SP1ProofRequest,
    ) -> SP1ReceiptArtifact:

        return SP1ReceiptArtifact(
            receipt_id=(
                f"receipt-{request.request_id}"
            ),

            request_id=(
                request.request_id
            ),

            proof_hash=(
                f"proof-{request.request_id}"
            ),

            verification_key_hash=(
                f"vk-{request.program_id}"
            ),
        )
