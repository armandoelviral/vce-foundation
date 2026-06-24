from dataclasses import dataclass

from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)


@dataclass(frozen=True)
class ValidityState:
    total_records: int
    total_days: int

    @classmethod
    def from_records(
        cls,
        records: list[ValidityRecord],
    ):
        return cls(
            total_records=len(records),
            total_days=sum(
                record.valid_days
                for record in records
            ),
        )
