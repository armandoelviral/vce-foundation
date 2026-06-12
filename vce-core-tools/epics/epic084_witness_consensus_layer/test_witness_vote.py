from epics.epic084_witness_consensus_layer.witness_vote import (
    WitnessVote,
)


def build_vote(
    witness_id="rekor",
    observed=True,
):

    return WitnessVote(
        witness_id=witness_id,
        ledger_root_hash="root-hash-001",
        anchor_reference="anchor-ref-001",
        observed=observed,
        observed_at="2026-06-10T00:00:00Z",
    )


def test_witness_vote_creation():

    vote = build_vote()

    assert vote.witness_id == "rekor"
    assert vote.ledger_root_hash == "root-hash-001"
    assert vote.observed is True


def test_witness_vote_can_represent_failed_observation():

    vote = build_vote(
        witness_id="opentimestamps",
        observed=False,
    )

    assert vote.witness_id == "opentimestamps"
    assert vote.observed is False


def test_witness_vote_serializes_to_dict():

    vote = build_vote()

    payload = vote.to_dict()

    assert payload["witness_id"] == "rekor"
    assert payload["ledger_root_hash"] == "root-hash-001"
    assert payload["anchor_reference"] == "anchor-ref-001"
    assert payload["observed"] is True
