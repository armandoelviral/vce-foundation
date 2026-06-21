from phase4.real_sp1_sdk_integration.sp1_receipt_loader import (
    SP1ReceiptLoader,
)

from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


def test_loader_returns_receipt():

    loader = SP1ReceiptLoader()

    receipt = loader.load(
        receipt_path="receipt.bin"
    )

    assert isinstance(
        receipt,
        SP1ReceiptArtifact,
    )


def test_loader_contains_receipt_id():

    loader = SP1ReceiptLoader()

    receipt = loader.load(
        receipt_path="receipt.bin"
    )

    assert (
        receipt.receipt_id
        == "receipt.bin"
    )


def test_loader_contains_proof_hash():

    loader = SP1ReceiptLoader()

    receipt = loader.load(
        receipt_path="receipt.bin"
    )

    assert (
        receipt.proof_hash
        == "loaded-proof-hash"
    )


def test_loader_contains_vk_hash():

    loader = SP1ReceiptLoader()

    receipt = loader.load(
        receipt_path="receipt.bin"
    )

    assert (
        receipt.verification_key_hash
        == "loaded-vk-hash"
    )
