from dataclasses import dataclass

from epics.phase6_001_constitutional_identity.identity_record import (
    IdentityRecord,
)


@dataclass(frozen=True)
class IdentityState:
    total_identities: int

    @classmethod
    def from_records(
        cls,
        records: list[IdentityRecord],
    ):
        return cls(
            total_identities=len(records)
        )
