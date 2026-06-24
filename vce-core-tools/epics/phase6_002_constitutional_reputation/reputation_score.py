from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)


def calculate_reputation_score(
    records: list[ReputationRecord],
):
    return sum(
        record.score_delta
        for record in records
    )
