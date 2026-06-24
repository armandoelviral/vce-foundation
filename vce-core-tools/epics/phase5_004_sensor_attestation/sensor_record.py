from dataclasses import dataclass


@dataclass(frozen=True)
class SensorRecord:
    sensor_id: str
    sensor_type: str
    manufacturer: str

    def __post_init__(self):
        if not self.sensor_id:
            raise ValueError("sensor_id is required")

        if not self.sensor_type:
            raise ValueError("sensor_type is required")

        if not self.manufacturer:
            raise ValueError("manufacturer is required")
