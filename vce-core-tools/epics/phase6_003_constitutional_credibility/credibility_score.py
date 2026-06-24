from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)


def calculate_credibility_score(
    records: list[CredibilityRecord],
):
    return sum(
        record.credibility_delta
        for record in records
    )
