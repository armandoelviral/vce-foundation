from epics.phase5_004_sensor_attestation.sensor_record import SensorRecord
from epics.phase5_004_sensor_attestation.sensor_registry import SensorRegistry


def test_registry_stores_sensor():
    registry = SensorRegistry()

    registry.add(
        SensorRecord(
            "sensor.001",
            "camera",
            "trusted_vendor",
        )
    )

    assert len(registry.records()) == 1


def test_rejects_duplicate_sensor():
    registry = SensorRegistry()

    sensor = SensorRecord(
        "sensor.001",
        "camera",
        "trusted_vendor",
    )

    registry.add(sensor)

    try:
        registry.add(sensor)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = SensorRegistry()

    registry.add(
        SensorRecord(
            "sensor.001",
            "camera",
            "trusted_vendor",
        )
    )

    items = registry.records()
    items.clear()

    assert len(registry.records()) == 1
