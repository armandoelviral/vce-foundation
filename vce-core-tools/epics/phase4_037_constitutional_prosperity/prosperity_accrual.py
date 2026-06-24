from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


def calculate_total_prosperity(
    records: list[ProsperityRecord],
):
    return sum(record.prosperity_amount for record in records)
