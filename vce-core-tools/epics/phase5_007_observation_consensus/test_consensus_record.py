from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)


def test_consensus_record_creation():
    record = ConsensusRecord(
        consensus_id="consensus.001",
        claim_id="claim.001",
        observer_id="observer.001",
        vote=True,
    )

    assert record.vote is True


def test_requires_consensus_id():
    try:
        ConsensusRecord(
            "",
            "claim.001",
            "observer.001",
            True,
        )
        assert False
    except ValueError:
        assert True
