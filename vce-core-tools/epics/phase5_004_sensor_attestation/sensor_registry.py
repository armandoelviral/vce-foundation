from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)


class SensorRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: SensorRecord):
        if record.sensor_id in self._ids:
            raise ValueError("duplicate sensor")

        self._records.append(record)
        self._ids.add(record.sensor_id)

    def records(self):
        return list(self._records)
