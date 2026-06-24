from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)


class WitnessRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: WitnessRecord):
        if record.witness_id in self._ids:
            raise ValueError(
                "duplicate witness"
            )

        self._records.append(record)
        self._ids.add(record.witness_id)

    def records(self):
        return list(self._records)
