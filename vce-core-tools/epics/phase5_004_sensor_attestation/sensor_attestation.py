from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)


def attest_sensor(sensor: SensorRecord):
    return {
        "attested": True,
        "sensor_id": sensor.sensor_id,
        "sensor_type": sensor.sensor_type,
    }
