from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)
from epics.phase5_007_observation_consensus.consensus_state import (
    ConsensusState,
)


def test_builds_consensus_state():
    records = [
        ConsensusRecord("c1", "claim.001", "observer.001", True),
        ConsensusRecord("c2", "claim.001", "observer.002", True),
        ConsensusRecord("c3", "claim.001", "observer.003", False),
    ]

    state = ConsensusState.from_records(records)

    assert state.total_votes == 3
    assert state.yes_votes == 2
    assert state.no_votes == 1


def test_empty_consensus_state():
    state = ConsensusState.from_records([])

    assert state.total_votes == 0
    assert state.yes_votes == 0
    assert state.no_votes == 0
