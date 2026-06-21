from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.real_sp1_sdk_integration.native_sp1_proof_generation import (
    NativeSP1ProofGeneration,
)

from phase4.real_sp1_sdk_integration.real_receipt_verification_pipeline import (
    RealReceiptVerificationPipeline,
)


def test_pipeline_verifies_receipt():

    pipeline = (
        RealReceiptVerificationPipeline(
            SP1SDKConfig(
                sdk_path="sp1",
                elf_path="program.elf",
                prover_mode="local",
            )
        )
    )

    assert pipeline.run() is True


def test_pipeline_returns_boolean():

    pipeline = (
        RealReceiptVerificationPipeline(
            SP1SDKConfig(
                sdk_path="sp1",
                elf_path="program.elf",
                prover_mode="local",
            )
        )
    )

    result = pipeline.run()

    assert isinstance(
        result,
        bool,
    )


def test_pipeline_generates_receipt():

    generator = NativeSP1ProofGeneration(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    receipt = generator.generate()

    assert receipt.receipt_id == "receipt.bin"
