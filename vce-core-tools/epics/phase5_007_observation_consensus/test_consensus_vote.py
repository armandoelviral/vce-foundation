from epics.phase5_007_observation_consensus.consensus_vote import (
    calculate_consensus,
)
from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)


def test_majority_vote():
    records = [
        ConsensusRecord("1","c","o1",True),
        ConsensusRecord("2","c","o2",True),
        ConsensusRecord("3","c","o3",False),
    ]

    result = calculate_consensus(records)

    assert result["accepted"] is True
