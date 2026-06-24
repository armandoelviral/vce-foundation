from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)


class ObservationRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: ObservationRecord):
        if record.observation_id in self._ids:
            raise ValueError(
                "duplicate observation"
            )

        self._records.append(record)
        self._ids.add(record.observation_id)

    def records(self):
        return list(self._records)
