from dataclasses import dataclass

from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)


@dataclass(frozen=True)
class CivilizationReplayState:
    total_records: int
    latest_epoch: int

    @classmethod
    def from_records(
        cls,
        records: list[CivilizationReplayRecord],
    ):
        return cls(
            total_records=len(records),
            latest_epoch=max(
                (record.epoch for record in records),
                default=0,
            ),
        )
