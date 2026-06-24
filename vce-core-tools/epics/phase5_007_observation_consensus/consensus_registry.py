from epics.phase5_007_observation_consensus.consensus_record import (
    ConsensusRecord,
)


class ConsensusRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: ConsensusRecord):
        if record.consensus_id in self._ids:
            raise ValueError("duplicate consensus")

        self._records.append(record)
        self._ids.add(record.consensus_id)

    def records(self):
        return list(self._records)
