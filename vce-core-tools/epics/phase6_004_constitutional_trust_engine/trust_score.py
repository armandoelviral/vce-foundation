from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)


def calculate_trust_score(
    records: list[TrustRecord],
):
    return sum(
        record.trust_delta
        for record in records
    )
