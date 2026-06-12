from epics.epic084_witness_consensus_layer.consensus_attestation import (
    build_consensus_attestation,
)
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


def test_end_to_end_consensus_flow_achieves_consensus():

    collection = WitnessCollection(
        votes=[
            build_vote("rekor", True),
            build_vote("private-log", True),
            build_vote("opentimestamps", False),
        ]
    )

    policy = ConsensusPolicy(
        policy_id="policy-2-of-3",
        required_votes=2,
        total_witnesses=3,
    )

    evaluation = evaluate_consensus(
        collection,
        policy,
    )

    attestation = build_consensus_attestation(
        ledger_root_hash="root-hash-001",
        evaluation=evaluation,
    )

    assert evaluation["consensus"] == "CONSENSUS_ACHIEVED"
    assert attestation.consensus == "CONSENSUS_ACHIEVED"
    assert attestation.policy == "2-of-3"
    assert attestation.observed_votes == 2
    assert attestation.total_votes == 3


def test_end_to_end_consensus_flow_rejects_insufficient_witnesses():

    collection = WitnessCollection(
        votes=[
            build_vote("rekor", True),
            build_vote("private-log", False),
            build_vote("opentimestamps", False),
        ]
    )

    policy = ConsensusPolicy(
        policy_id="policy-2-of-3",
        required_votes=2,
        total_witnesses=3,
    )

    evaluation = evaluate_consensus(
        collection,
        policy,
    )

    attestation = build_consensus_attestation(
        ledger_root_hash="root-hash-001",
        evaluation=evaluation,
    )

    assert evaluation["consensus"] == "CONSENSUS_NOT_ACHIEVED"
    assert attestation.consensus == "CONSENSUS_NOT_ACHIEVED"
    assert attestation.observed_votes == 1
    assert attestation.policy == "2-of-3"
