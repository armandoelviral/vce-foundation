from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)


def test_observation_record_creation():
    record = ObservationRecord(
        observation_id="obs.001",
        observer_id="observer.001",
        observation_type="physical",
        observation_value="object_detected",
    )

    assert record.observation_id == "obs.001"
    assert record.observer_id == "observer.001"


def test_rejects_empty_observation_id():
    try:
        ObservationRecord(
            observation_id="",
            observer_id="observer.001",
            observation_type="physical",
            observation_value="value",
        )
        assert False
    except ValueError as exc:
        assert "observation_id" in str(exc)


def test_rejects_empty_observer():
    try:
        ObservationRecord(
            observation_id="obs.001",
            observer_id="",
            observation_type="physical",
            observation_value="value",
        )
        assert False
    except ValueError as exc:
        assert "observer_id" in str(exc)
