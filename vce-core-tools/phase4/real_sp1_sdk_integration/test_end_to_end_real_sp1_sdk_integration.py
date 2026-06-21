from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.real_sp1_sdk_integration.d5_d7_native_proof_flow import (
    D5D7NativeProofFlow,
)


def test_end_to_end_real_sp1_sdk_integration():

    flow = D5D7NativeProofFlow(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    assert flow.run() is True


def test_end_to_end_returns_boolean():

    flow = D5D7NativeProofFlow(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    result = flow.run()

    assert isinstance(
        result,
        bool,
    )
