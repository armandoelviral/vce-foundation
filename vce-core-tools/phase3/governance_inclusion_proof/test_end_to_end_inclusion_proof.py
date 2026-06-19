from phase3.governance_inclusion_proof.inclusion_proof_record import (
    InclusionProofRecord,
)

from phase3.governance_inclusion_proof.proof_registry import (
    ProofRegistry,
)

from phase3.governance_inclusion_proof.proof_evaluation import (
    ProofEvaluation,
)

from phase3.governance_inclusion_proof.proof_decision import (
    ProofDecision,
)

from phase3.governance_inclusion_proof.proof_query import (
    ProofQuery,
)

from phase3.governance_inclusion_proof.proof_report import (
    ProofReport,
)

from phase3.governance_inclusion_proof.proof_attestation import (
    ProofAttestation,
)


def test_end_to_end_inclusion_proof():

    registry = ProofRegistry()

    proof = InclusionProofRecord(
        leaf_id="leaf-001",
        root_id="root-001",
        proof_hash="proof-hash-001",
    )

    registry.add(
        proof_id="proof-001",
        proof=proof,
    )

    evaluation = (
        ProofEvaluation.evaluate(
            proof
        )
    )

    assert evaluation is True

    decision = (
        ProofDecision.from_evaluation(
            evaluation
        )
    )

    assert (
        decision.status
        == "ACCEPT_PROOF"
    )

    query = ProofQuery(
        registry
    )

    recovered = query.by_id(
        "proof-001"
    )

    assert recovered == proof

    report = ProofReport(
        {
            "proof-001":
                recovered
        }
    )

    assert report.proof_count() == 1

    assert report.proof_ids() == [
        "proof-001"
    ]

    attestation = (
        ProofAttestation.attest(
            attestation_id="att-001",
            proof=proof,
        )
    )

    assert (
        attestation.subject
        == "governance_inclusion_proof"
    )

    assert (
        attestation.evidence_hash
        == "proof-hash-001"
    )
