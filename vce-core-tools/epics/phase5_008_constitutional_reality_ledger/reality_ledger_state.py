from dataclasses import dataclass

from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)


@dataclass(frozen=True)
class RealityLedgerState:
    total_entries: int

    @classmethod
    def from_records(
        cls,
        records: list[RealityLedgerRecord],
    ):
        return cls(
            total_entries=len(records)
        )
