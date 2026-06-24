from epics.phase4_t0_constitutional_trust.trust_record import (
    TrustRecord,
)


def calculate_total_trust(
    records: list[TrustRecord],
) -> int:
    return sum(
        record.trust_amount
        for record in records
    )
