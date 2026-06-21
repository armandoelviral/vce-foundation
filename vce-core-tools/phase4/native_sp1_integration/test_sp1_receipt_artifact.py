from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


def test_contains_receipt_id():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        receipt.receipt_id
        == "receipt-001"
    )


def test_contains_request_id():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        receipt.request_id
        == "proof-001"
    )


def test_contains_proof_hash():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        receipt.proof_hash
        == "proof-hash-001"
    )


def test_contains_verification_key_hash():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        receipt.verification_key_hash
        == "vk-hash-001"
    )


def test_serializes():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert receipt.to_dict() == {
        "receipt_id":
            "receipt-001",

        "request_id":
            "proof-001",

        "proof_hash":
            "proof-hash-001",

        "verification_key_hash":
            "vk-hash-001",
    }
