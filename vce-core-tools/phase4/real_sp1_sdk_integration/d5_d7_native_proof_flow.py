from phase4.real_sp1_sdk_integration.native_sp1_proof_generation import (
    NativeSP1ProofGeneration,
)

from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.native_sp1_integration.sp1_receipt_verification import (
    SP1ReceiptVerification,
)

from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)

from phase4.native_sp1_integration.d7_real_browser_verification import (
    D7RealBrowserVerification,
)


class D5D7NativeProofFlow:

    def __init__(
        self,
        config: SP1SDKConfig,
    ):

        self.config = config

    def run(
        self,
    ) -> bool:

        receipt = (
            NativeSP1ProofGeneration(
                self.config
            ).generate()
        )

        if not (
            SP1ReceiptVerification.verify(
                receipt
            )
        ):
            return False

        attachment = (
            D5RealProofAttachment.attach(
                d5_artifact_id="d5-001",
                receipt=receipt,
            )
        )

        return (
            D7RealBrowserVerification.verify(
                attachment
            )
        )
