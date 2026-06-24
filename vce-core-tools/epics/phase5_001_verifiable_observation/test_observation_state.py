from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)
from epics.phase5_001_verifiable_observation.observation_state import (
    ObservationState,
)


def test_builds_observation_state():
    records = [
        ObservationRecord(
            "obs.001",
            "observer.001",
            "physical",
            "object_detected",
        )
    ]

    state = ObservationState.from_records(records)

    assert state.total_observations == 1


def test_empty_observation_state():
    state = ObservationState.from_records([])

    assert state.total_observations == 0
