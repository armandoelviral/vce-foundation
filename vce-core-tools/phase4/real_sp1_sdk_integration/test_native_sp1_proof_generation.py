from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.real_sp1_sdk_integration.native_sp1_proof_generation import (
    NativeSP1ProofGeneration,
)

from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


def test_generates_receipt():

    generator = NativeSP1ProofGeneration(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    receipt = generator.generate()

    assert isinstance(
        receipt,
        SP1ReceiptArtifact,
    )


def test_receipt_contains_receipt_id():

    generator = NativeSP1ProofGeneration(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    receipt = generator.generate()

    assert (
        receipt.receipt_id
        == "receipt.bin"
    )


def test_receipt_contains_proof_hash():

    generator = NativeSP1ProofGeneration(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    receipt = generator.generate()

    assert (
        receipt.proof_hash
        == "loaded-proof-hash"
    )


def test_receipt_contains_vk_hash():

    generator = NativeSP1ProofGeneration(
        SP1SDKConfig(
            sdk_path="sp1",
            elf_path="program.elf",
            prover_mode="local",
        )
    )

    receipt = generator.generate()

    assert (
        receipt.verification_key_hash
        == "loaded-vk-hash"
    )
