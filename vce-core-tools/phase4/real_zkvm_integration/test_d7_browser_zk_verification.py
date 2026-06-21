from phase4.real_zkvm_integration.d5_zk_proof_attachment import (
    D5zkProofAttachment,
)

from phase4.real_zkvm_integration.d7_browser_zk_verification import (
    D7BrowserZkVerification,
)


def test_valid_attachment_verifies():

    attachment = D5zkProofAttachment(
        d5_artifact_id="d5-001",
        proof_artifact_id="artifact-001",
        proof_hash="proof-001",
    )

    assert (
        D7BrowserZkVerification.verify(
            attachment
        )
        is True
    )


def test_missing_d5_artifact_fails():

    attachment = D5zkProofAttachment(
        d5_artifact_id="",
        proof_artifact_id="artifact-001",
        proof_hash="proof-001",
    )

    assert (
        D7BrowserZkVerification.verify(
            attachment
        )
        is False
    )


def test_missing_artifact_id_fails():

    attachment = D5zkProofAttachment(
        d5_artifact_id="d5-001",
        proof_artifact_id="",
        proof_hash="proof-001",
    )

    assert (
        D7BrowserZkVerification.verify(
            attachment
        )
        is False
    )


def test_missing_proof_hash_fails():

    attachment = D5zkProofAttachment(
        d5_artifact_id="d5-001",
        proof_artifact_id="artifact-001",
        proof_hash="",
    )

    assert (
        D7BrowserZkVerification.verify(
            attachment
        )
        is False
    )
