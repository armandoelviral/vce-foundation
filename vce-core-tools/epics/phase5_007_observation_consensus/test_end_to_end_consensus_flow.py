from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)
from epics.phase5_007_observation_consensus.consensus_registry import (
    ConsensusRegistry,
)
from epics.phase5_007_observation_consensus.consensus_state import (
    ConsensusState,
)
from epics.phase5_007_observation_consensus.consensus_verifier import (
    verify_consensus_state,
)


def test_end_to_end_consensus_flow():
    registry = ConsensusRegistry()

    registry.add(ConsensusRecord("c1", "claim.001", "observer.001", True))
    registry.add(ConsensusRecord("c2", "claim.001", "observer.002", True))
    registry.add(ConsensusRecord("c3", "claim.001", "observer.003", False))

    state = ConsensusState.from_records(registry.records())

    verification = verify_consensus_state(state)

    assert verification["verified"] is True
    assert verification["yes_votes"] == 2
    assert verification["total_votes"] == 3
