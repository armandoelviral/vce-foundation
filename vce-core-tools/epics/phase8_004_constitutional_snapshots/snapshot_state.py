from dataclasses import dataclass

from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)


@dataclass(frozen=True)
class SnapshotState:
    total_snapshots: int
    latest_epoch: int

    @classmethod
    def from_records(
        cls,
        records: list[SnapshotRecord],
    ):
        return cls(
            total_snapshots=len(records),
            latest_epoch=max(
                (record.epoch for record in records),
                default=0,
            ),
        )
