from dataclasses import dataclass

from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)


@dataclass(frozen=True)
class TimeAuditState:
    total_records: int
    latest_epoch: int

    @classmethod
    def from_records(
        cls,
        records: list[TimeAuditRecord],
    ):
        return cls(
            total_records=len(records),
            latest_epoch=max(
                (record.epoch for record in records),
                default=0,
            ),
        )
