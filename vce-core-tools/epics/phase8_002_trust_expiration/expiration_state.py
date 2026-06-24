from dataclasses import dataclass

from epics.phase8_002_trust_expiration.expiration_record import (
    ExpirationRecord,
)


@dataclass(frozen=True)
class ExpirationState:
    total_records: int
    total_remaining_days: int

    @classmethod
    def from_records(
        cls,
        records: list[ExpirationRecord],
    ):
        return cls(
            total_records=len(records),
            total_remaining_days=sum(
                record.remaining_days
                for record in records
            ),
        )
