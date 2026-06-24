from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


def calculate_allocated_reserves(
    records: list[TreasuryRecord],
) -> int:
    return sum(
        record.allocation_amount
        for record in records
    )
