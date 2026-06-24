from dataclasses import dataclass

from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)


@dataclass(frozen=True)
class ReplayState:
    total_records: int
    max_epoch: int

    @classmethod
    def from_records(
        cls,
        records: list[ReplayRecord],
    ):
        return cls(
            total_records=len(records),
            max_epoch=max(
                (
                    record.historical_epoch
                    for record in records
                ),
                default=0,
            ),
        )
