from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)

from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)


def test_contains_d5_artifact_id():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    attachment = D5RealProofAttachment.attach(
        d5_artifact_id="d5-001",
        receipt=receipt,
    )

    assert attachment.d5_artifact_id == "d5-001"


def test_contains_receipt_id():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    attachment = D5RealProofAttachment.attach(
        d5_artifact_id="d5-001",
        receipt=receipt,
    )

    assert attachment.receipt_id == "receipt-001"


def test_contains_proof_hash():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    attachment = D5RealProofAttachment.attach(
        d5_artifact_id="d5-001",
        receipt=receipt,
    )

    assert attachment.proof_hash == "proof-hash-001"


def test_contains_vk_hash():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    attachment = D5RealProofAttachment.attach(
        d5_artifact_id="d5-001",
        receipt=receipt,
    )

    assert (
        attachment.verification_key_hash
        == "vk-hash-001"
    )


def test_serializes():

    receipt = SP1ReceiptArtifact(
        receipt_id="receipt-001",
        request_id="proof-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    attachment = D5RealProofAttachment.attach(
        d5_artifact_id="d5-001",
        receipt=receipt,
    )

    assert attachment.to_dict() == {
        "d5_artifact_id": "d5-001",
        "receipt_id": "receipt-001",
        "proof_hash": "proof-hash-001",
        "verification_key_hash": "vk-hash-001",
    }
