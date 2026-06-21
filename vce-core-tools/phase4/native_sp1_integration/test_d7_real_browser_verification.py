from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)

from phase4.native_sp1_integration.d7_real_browser_verification import (
    D7RealBrowserVerification,
)


def test_valid_attachment_verifies():

    attachment = D5RealProofAttachment(
        d5_artifact_id="d5-001",
        receipt_id="receipt-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is True
    )


def test_missing_d5_artifact_fails():

    attachment = D5RealProofAttachment(
        d5_artifact_id="",
        receipt_id="receipt-001",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is False
    )


def test_missing_receipt_id_fails():

    attachment = D5RealProofAttachment(
        d5_artifact_id="d5-001",
        receipt_id="",
        proof_hash="proof-hash-001",
        verification_key_hash="vk-hash-001",
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is False
    )


def test_missing_proof_hash_fails():

    attachment = D5RealProofAttachment(
        d5_artifact_id="d5-001",
        receipt_id="receipt-001",
        proof_hash="",
        verification_key_hash="vk-hash-001",
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is False
    )


def test_missing_vk_hash_fails():

    attachment = D5RealProofAttachment(
        d5_artifact_id="d5-001",
        receipt_id="receipt-001",
        proof_hash="proof-hash-001",
        verification_key_hash="",
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is False
    )
