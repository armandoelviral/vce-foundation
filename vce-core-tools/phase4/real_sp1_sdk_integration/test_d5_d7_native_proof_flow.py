from phase4.real_sp1_sdk_integration.sp1_sdk_config import (
    SP1SDKConfig,
)

from phase4.real_sp1_sdk_integration.native_sp1_proof_generation import (
    NativeSP1ProofGeneration,
)

from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)

from phase4.native_sp1_integration.d7_real_browser_verification import (
    D7RealBrowserVerification,
)

from phase4.native_sp1_integration.sp1_receipt_verification import (
    SP1ReceiptVerification,
)


def test_native_flow_verifies_end_to_end():

    receipt = (
        NativeSP1ProofGeneration(
            SP1SDKConfig(
                sdk_path="sp1",
                elf_path="program.elf",
                prover_mode="local",
            )
        ).generate()
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is True
    )

    attachment = (
        D5RealProofAttachment.attach(
            d5_artifact_id="d5-001",
            receipt=receipt,
        )
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is True
    )


def test_attachment_contains_receipt():

    receipt = (
        NativeSP1ProofGeneration(
            SP1SDKConfig(
                sdk_path="sp1",
                elf_path="program.elf",
                prover_mode="local",
            )
        ).generate()
    )

    attachment = (
        D5RealProofAttachment.attach(
            d5_artifact_id="d5-001",
            receipt=receipt,
        )
    )

    assert (
        attachment.receipt_id
        == "receipt.bin"
    )


def test_attachment_contains_proof_hash():

    receipt = (
        NativeSP1ProofGeneration(
            SP1SDKConfig(
                sdk_path="sp1",
                elf_path="program.elf",
                prover_mode="local",
            )
        ).generate()
    )

    attachment = (
        D5RealProofAttachment.attach(
            d5_artifact_id="d5-001",
            receipt=receipt,
        )
    )

    assert (
        attachment.proof_hash
        == "loaded-proof-hash"
    )
