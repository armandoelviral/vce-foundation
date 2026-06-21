from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)

from phase4.native_sp1_integration.sp1_receipt_verification import (
    SP1ReceiptVerification,
)


def test_valid_receipt_verifies():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is True
    )


def test_missing_receipt_id_fails():

    receipt = SP1ReceiptArtifact(
        receipt_id="",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is False
    )


def test_missing_request_id_fails():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is False
    )


def test_missing_proof_hash_fails():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="",
        verification_key_hash="vk-hash-001",
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is False
    )


def test_missing_vk_hash_fails():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="",
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is False
    )
