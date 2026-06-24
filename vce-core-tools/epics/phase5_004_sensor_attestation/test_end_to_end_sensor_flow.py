from epics.phase5_004_sensor_attestation.sensor_attestation import (
    attest_sensor,
)
from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)
from epics.phase5_004_sensor_attestation.sensor_registry import (
    SensorRegistry,
)


def test_end_to_end_sensor_flow():
    registry = SensorRegistry()

    registry.add(
        SensorRecord(
            "sensor.001",
            "camera",
            "trusted_vendor",
        )
    )

    result = attest_sensor(
        registry.records()[0]
    )

    assert result["attested"] is True
    assert result["sensor_id"] == "sensor.001"
