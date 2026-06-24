from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)
from epics.phase5_007_observation_consensus.consensus_registry import (
    ConsensusRegistry,
)


def test_registry_adds_record():
    registry = ConsensusRegistry()

    registry.add(
        ConsensusRecord(
            "c1",
            "claim.001",
            "observer.001",
            True,
        )
    )

    assert len(registry.records()) == 1
