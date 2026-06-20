from phase4.hot_consensus_cold_proof.transparency_proof_anchor import (
    TransparencyProofAnchor,
)

from phase4.hot_consensus_cold_proof.browser_proof_verification import (
    BrowserProofVerification,
)


def test_valid_anchor_verifies():

    anchor = TransparencyProofAnchor(
        anchor_id="anchor-001",
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    assert (
        BrowserProofVerification.verify(anchor)
        is True
    )


def test_missing_anchor_id_fails():

    anchor = TransparencyProofAnchor(
        anchor_id="",
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    assert (
        BrowserProofVerification.verify(anchor)
        is False
    )


def test_missing_execution_request_id_fails():

    anchor = TransparencyProofAnchor(
        anchor_id="anchor-001",
        execution_request_id="",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    assert (
        BrowserProofVerification.verify(anchor)
        is False
    )


def test_missing_result_id_fails():

    anchor = TransparencyProofAnchor(
        anchor_id="anchor-001",
        execution_request_id="request-001",
        result_id="",
        proof_hash="proof-hash-001",
    )

    assert (
        BrowserProofVerification.verify(anchor)
        is False
    )


def test_missing_proof_hash_fails():

    anchor = TransparencyProofAnchor(
        anchor_id="anchor-001",
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="",
    )

    assert (
        BrowserProofVerification.verify(anchor)
        is False
    )
