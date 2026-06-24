from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)


def audit_observations(
    records: list[ObservationRecord],
):
    return {
        "observation_count": len(records),
    }
