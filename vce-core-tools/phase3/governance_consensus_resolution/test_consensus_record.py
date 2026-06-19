from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)


def test_contains_consensus_id():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    assert (
        record.consensus_id
        == "consensus-001"
    )


def test_contains_proposal_id():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    assert (
        record.proposal_id
        == "proposal-001"
    )


def test_contains_outcome():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    assert (
        record.outcome
        == "APPROVED"
    )


def test_serializes():

    record = ConsensusRecord(
        consensus_id="consensus-001",
        proposal_id="proposal-001",
        outcome="APPROVED",
    )

    assert record.to_dict() == {
        "consensus_id":
            "consensus-001",

        "proposal_id":
            "proposal-001",

        "outcome":
            "APPROVED",
    }
