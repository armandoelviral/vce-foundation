from dataclasses import dataclass

from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)


@dataclass(frozen=True)
class DurabilityState:
    total_records: int
    total_years: int

    @classmethod
    def from_records(
        cls,
        records: list[DurabilityRecord],
    ):
        return cls(
            total_records=len(records),
            total_years=sum(
                record.durability_years
                for record in records
            ),
        )
