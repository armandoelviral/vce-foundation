from dataclasses import dataclass

from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)


@dataclass(frozen=True)
class RetentionState:
    total_records: int
    total_years: int

    @classmethod
    def from_records(
        cls,
        records: list[RetentionRecord],
    ):
        return cls(
            total_records=len(records),
            total_years=sum(
                record.retention_years
                for record in records
            ),
        )
