from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


def calculate_total_reserves(
    records: list[ReserveRecord],
) -> int:
    return sum(
        record.reserve_amount
        for record in records
    )
