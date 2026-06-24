from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


class StabilityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: StabilityRecord):
        if record.stability_id in self._ids:
            raise ValueError(
                "duplicate stability"
            )

        self._records.append(record)
        self._ids.add(record.stability_id)

    def records(self):
        return list(self._records)
