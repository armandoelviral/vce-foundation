from epics.phase5_004_sensor_attestation.sensor_attestation import (
    attest_sensor,
)
from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)


def test_attests_sensor():
    sensor = SensorRecord(
        "sensor.001",
        "camera",
        "trusted_vendor",
    )

    result = attest_sensor(sensor)

    assert result["attested"] is True


def test_contains_sensor_id():
    sensor = SensorRecord(
        "sensor.001",
        "camera",
        "trusted_vendor",
    )

    result = attest_sensor(sensor)

    assert result["sensor_id"] == "sensor.001"
