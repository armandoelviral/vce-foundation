from dataclasses import dataclass

from epics.phase5_004_sensor_attestation.sensor_record import (
    SensorRecord,
)


@dataclass(frozen=True)
class SensorState:
    total_sensors: int

    @classmethod
    def from_records(
        cls,
        records: list[SensorRecord],
    ):
        return cls(
            total_sensors=len(records)
        )
