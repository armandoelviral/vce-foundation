from phase3.governance_consensus_resolution.consensus_record import (
    ConsensusRecord,
)


class ConsensusRegistry:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: ConsensusRecord,
    ) -> None:

        self._records[
            record.consensus_id
        ] = record

    def get(
        self,
        consensus_id: str,
    ):

        return self._records.get(
            consensus_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def consensus_ids(
        self,
    ):

        return list(
            self._records.keys()
        )
