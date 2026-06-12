from epics.epic084_witness_consensus_layer.consensus_evaluator import (
    evaluate_consensus,
)
from epics.epic084_witness_consensus_layer.consensus_policy import (
    ConsensusPolicy,
)
from epics.epic084_witness_consensus_layer.witness_collection import (
    WitnessCollection,
)
from epics.epic084_witness_consensus_layer.witness_vote import (
    WitnessVote,
)


def build_vote(
    witness_id,
    observed,
):

    return WitnessVote(
        witness_id=witness_id,
        ledger_root_hash="root-hash-001",
        anchor_reference=f"anchor-ref-{witness_id}",
        observed=observed,
        observed_at="2026-06-10T00:00:00Z",
    )


def build_policy():

    return ConsensusPolicy(
        policy_id="policy-2-of-3",
        required_votes=2,
        total_witnesses=3,
    )


def test_consensus_evaluation_achieves_consensus():

    collection = WitnessCollection(
        votes=[
            build_vote("rekor", True),
            build_vote("private-log", True),
            build_vote("opentimestamps", False),
        ]
    )

    result = evaluate_consensus(
        collection,
        build_policy(),
    )

    assert result["consensus"] == "CONSENSUS_ACHIEVED"
    assert result["observed_votes"] == 2
    assert result["policy"] == "2-of-3"


def test_consensus_evaluation_rejects_insufficient_votes():

    collection = WitnessCollection(
        votes=[
            build_vote("rekor", True),
            build_vote("private-log", False),
            build_vote("opentimestamps", False),
        ]
    )

    result = evaluate_consensus(
        collection,
        build_policy(),
    )

    assert result["consensus"] == "CONSENSUS_NOT_ACHIEVED"
    assert result["observed_votes"] == 1
    assert result["policy"] == "2-of-3"


def test_consensus_evaluation_reports_total_votes():

    collection = WitnessCollection(
        votes=[
            build_vote("rekor", True),
            build_vote("private-log", True),
            build_vote("opentimestamps", True),
        ]
    )

    result = evaluate_consensus(
        collection,
        build_policy(),
    )

    assert result["total_votes"] == 3
