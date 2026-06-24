from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)


def test_sensor_record_creation():
    record = SensorRecord(
        sensor_id="sensor.001",
        sensor_type="camera",
        manufacturer="trusted_vendor",
    )

    assert record.sensor_id == "sensor.001"


def test_rejects_empty_sensor_id():
    try:
        SensorRecord(
            sensor_id="",
            sensor_type="camera",
            manufacturer="trusted_vendor",
        )
        assert False
    except ValueError as exc:
        assert "sensor_id" in str(exc)


def test_rejects_empty_sensor_type():
    try:
        SensorRecord(
            sensor_id="sensor.001",
            sensor_type="",
            manufacturer="trusted_vendor",
        )
        assert False
    except ValueError as exc:
        assert "sensor_type" in str(exc)
