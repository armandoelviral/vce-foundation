from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)

from phase3.governance_merkle_history.governance_merkle_registry import (
    GovernanceMerkleRegistry,
)

from phase3.governance_merkle_history.merkle_history_evaluation import (
    MerkleHistoryEvaluation,
)

from phase3.governance_merkle_history.merkle_history_decision import (
    MerkleHistoryDecision,
)

from phase3.governance_merkle_history.merkle_history_query import (
    MerkleHistoryQuery,
)

from phase3.governance_merkle_history.merkle_history_report import (
    MerkleHistoryReport,
)

from phase3.governance_merkle_history.governance_merkle_attestation import (
    GovernanceMerkleAttestation,
)


def test_end_to_end_governance_merkle_history():

    registry = GovernanceMerkleRegistry()

    leaf = GovernanceMerkleLeaf(
        leaf_id="leaf-001",
        snapshot_id="snap-001",
        hash_value="hash-001",
    )

    registry.add(leaf)

    evaluation = MerkleHistoryEvaluation.evaluate(
        leaf
    )

    assert evaluation is True

    decision = MerkleHistoryDecision.from_evaluation(
        evaluation
    )

    assert (
        decision.status
        == "ACCEPT_MERKLE"
    )

    query = MerkleHistoryQuery(
        registry
    )

    recovered = query.by_id(
        "leaf-001"
    )

    assert recovered == leaf

    report = MerkleHistoryReport(
        {
            "leaf-001": recovered
        }
    )

    assert report.leaf_count() == 1

    assert report.leaf_ids() == [
        "leaf-001"
    ]

    attestation = (
        GovernanceMerkleAttestation.attest(
            attestation_id="att-001",
            leaf=leaf,
        )
    )

    assert (
        attestation.subject
        == "governance_merkle_leaf"
    )

    assert (
        attestation.evidence_hash
        == "leaf-001"
    )
