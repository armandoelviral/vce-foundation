from phase4.real_sp1_sdk_integration.native_sp1_proof_generation import (
    NativeSP1ProofGeneration,
)

from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.native_sp1_integration.sp1_receipt_verification import (
    SP1ReceiptVerification,
)


class RealReceiptVerificationPipeline:

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

        return (
            SP1ReceiptVerification.verify(
                receipt
            )
        )
