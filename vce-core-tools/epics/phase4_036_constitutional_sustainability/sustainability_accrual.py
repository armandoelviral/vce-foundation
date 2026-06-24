from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


def calculate_total_sustainability(
    records: list[SustainabilityRecord],
):
    return sum(
        record.sustainability_amount
        for record in records
    )
