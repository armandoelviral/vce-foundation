from phase4.real_sp1_sdk_integration.sp1_command_builder import (
    SP1CommandBuilder,
)

from phase4.real_sp1_sdk_integration.sp1_process_runner import (
    SP1ProcessRunner,
)

from phase4.real_sp1_sdk_integration.sp1_receipt_loader import (
    SP1ReceiptLoader,
)

from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)


class NativeSP1ProofGeneration:

    def __init__(
        self,
        config: SP1SDKConfig,
    ):

        self.config = config

    def generate(
        self,
    ):

        command = (
            SP1CommandBuilder(
                self.config
            ).build()
        )

        SP1ProcessRunner().run(
            command
        )

        return (
            SP1ReceiptLoader().load(
                "receipt.bin"
            )
        )
