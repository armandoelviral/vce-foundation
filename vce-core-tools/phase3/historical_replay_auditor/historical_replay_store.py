from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)


class HistoricalReplayStore:

    def __init__(self):

        self._records = {}

    def add(
        self,
        record: HistoricalReplayRecord,
    ) -> None:

        self._records[
            record.replay_id
        ] = record

    def get(
        self,
        replay_id: str,
    ):

        return self._records.get(
            replay_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
