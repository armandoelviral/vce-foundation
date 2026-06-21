from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)


class SP1CommandBuilder:

    def __init__(
        self,
        config: SP1SDKConfig,
    ):

        self.config = config

    def build(
        self,
    ):

        return [
            self.config.sdk_path,
            "prove",
            self.config.elf_path,
        ]
