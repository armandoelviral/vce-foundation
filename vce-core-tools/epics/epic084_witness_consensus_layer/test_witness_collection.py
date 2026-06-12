from epics.epic084_witness_consensus_layer.witness_collection import (
    WitnessCollection,
)
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
        anchor_reference=f"anchor-ref-{witness_id}",
        observed=observed,
        observed_at="2026-06-10T00:00:00Z",
    )


def test_collection_starts_empty():

    collection = WitnessCollection()

    assert collection.total_count() == 0
    assert collection.observed_count() == 0


def test_collection_adds_vote():

    collection = WitnessCollection()

    collection.add_vote(
        build_vote()
    )

    assert collection.total_count() == 1


def test_collection_counts_observed_votes():

    collection = WitnessCollection()

    collection.add_vote(
        build_vote(
            witness_id="rekor",
            observed=True,
        )
    )

    collection.add_vote(
        build_vote(
            witness_id="opentimestamps",
            observed=False,
        )
    )

    assert collection.total_count() == 2
    assert collection.observed_count() == 1


def test_collection_returns_observed_votes():

    collection = WitnessCollection()

    collection.add_vote(
        build_vote(
            witness_id="rekor",
            observed=True,
        )
    )

    collection.add_vote(
        build_vote(
            witness_id="opentimestamps",
            observed=False,
        )
    )

    observed = collection.observed_votes()

    assert len(observed) == 1
    assert observed[0].witness_id == "rekor"


def test_collection_returns_all_votes_copy():

    collection = WitnessCollection()

    collection.add_vote(
        build_vote()
    )

    votes = collection.all_votes()

    assert len(votes) == 1
    assert votes[0].witness_id == "rekor"
