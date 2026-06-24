from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


def calculate_total_stability(
    records: list[StabilityRecord],
):
    return sum(
        record.stability_amount
        for record in records
    )
