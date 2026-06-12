from epics.epic084_witness_consensus_layer.consensus_attestation import (
    build_consensus_attestation,
)


def build_evaluation():

    return {
        "consensus": "CONSENSUS_ACHIEVED",
        "policy": "2-of-3",
        "observed_votes": 2,
        "total_votes": 3,
    }


def test_attestation_creation():

    attestation = (
        build_consensus_attestation(
            ledger_root_hash="root-hash-001",
            evaluation=build_evaluation(),
        )
    )

    assert (
        attestation.ledger_root_hash
        == "root-hash-001"
    )

    assert (
        attestation.consensus
        == "CONSENSUS_ACHIEVED"
    )


def test_attestation_contains_policy():

    attestation = (
        build_consensus_attestation(
            ledger_root_hash="root-hash-001",
            evaluation=build_evaluation(),
        )
    )

    assert (
        attestation.policy
        == "2-of-3"
    )


def test_attestation_contains_vote_counts():

    attestation = (
        build_consensus_attestation(
            ledger_root_hash="root-hash-001",
            evaluation=build_evaluation(),
        )
    )

    assert (
        attestation.observed_votes
        == 2
    )

    assert (
        attestation.total_votes
        == 3
    )


def test_attestation_serializes():

    attestation = (
        build_consensus_attestation(
            ledger_root_hash="root-hash-001",
            evaluation=build_evaluation(),
        )
    )

    payload = attestation.to_dict()

    assert (
        payload["ledger_root_hash"]
        == "root-hash-001"
    )

    assert (
        payload["consensus"]
        == "CONSENSUS_ACHIEVED"
    )
