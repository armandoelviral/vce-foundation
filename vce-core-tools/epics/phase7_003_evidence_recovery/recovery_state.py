from dataclasses import dataclass

from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)


@dataclass(frozen=True)
class RecoveryState:
    total_records: int
    total_recoveries: int

    @classmethod
    def from_records(
        cls,
        records: list[RecoveryRecord],
    ):
        return cls(
            total_records=len(records),
            total_recoveries=len(records),
        )
