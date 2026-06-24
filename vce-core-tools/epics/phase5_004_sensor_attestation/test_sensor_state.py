from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)
from epics.phase5_004_sensor_attestation.sensor_state import (
    SensorState,
)


def test_builds_sensor_state():
    state = SensorState.from_records(
        [
            SensorRecord(
                "sensor.001",
                "camera",
                "trusted_vendor",
            )
        ]
    )

    assert state.total_sensors == 1


def test_empty_sensor_state():
    state = SensorState.from_records([])

    assert state.total_sensors == 0
