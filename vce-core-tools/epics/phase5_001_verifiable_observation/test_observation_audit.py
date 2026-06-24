from epics.phase5_001_verifiable_observation.observation_audit import (
    audit_observations,
)
from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)


def test_observation_audit():
    records = [
        ObservationRecord(
            "obs.001",
            "observer.001",
            "physical",
            "object_detected",
        )
    ]

    audit = audit_observations(records)

    assert audit["observation_count"] == 1


def test_empty_audit():
    audit = audit_observations([])

    assert audit["observation_count"] == 0
