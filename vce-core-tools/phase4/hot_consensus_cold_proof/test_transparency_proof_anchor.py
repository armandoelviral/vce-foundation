from phase4.hot_consensus_cold_proof.proof_attachment import (
    ProofAttachment,
)

from phase4.hot_consensus_cold_proof.transparency_proof_anchor import (
    TransparencyProofAnchor,
)


def test_anchor_contains_anchor_id():

    attachment = ProofAttachment(
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    anchor = TransparencyProofAnchor.anchor(
        anchor_id="anchor-001",
        attachment=attachment,
    )

    assert anchor.anchor_id == "anchor-001"


def test_anchor_contains_execution_request_id():

    attachment = ProofAttachment(
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    anchor = TransparencyProofAnchor.anchor(
        anchor_id="anchor-001",
        attachment=attachment,
    )

    assert anchor.execution_request_id == "request-001"


def test_anchor_contains_proof_hash():

    attachment = ProofAttachment(
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    anchor = TransparencyProofAnchor.anchor(
        anchor_id="anchor-001",
        attachment=attachment,
    )

    assert anchor.proof_hash == "proof-hash-001"


def test_anchor_serializes():

    attachment = ProofAttachment(
        execution_request_id="request-001",
        result_id="result-001",
        proof_hash="proof-hash-001",
    )

    anchor = TransparencyProofAnchor.anchor(
        anchor_id="anchor-001",
        attachment=attachment,
    )

    assert anchor.to_dict() == {
        "anchor_id": "anchor-001",
        "execution_request_id": "request-001",
        "result_id": "result-001",
        "proof_hash": "proof-hash-001",
    }
