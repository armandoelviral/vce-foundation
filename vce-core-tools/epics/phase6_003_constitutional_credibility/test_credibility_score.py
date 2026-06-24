from epics.phase6_003_constitutional_credibility.credibility_record import (
    CredibilityRecord,
)
from epics.phase6_003_constitutional_credibility.credibility_score import (
    calculate_credibility_score,
)


def test_calculates_score():
    records = [
        CredibilityRecord("c1", "id1", 10),
        CredibilityRecord("c2", "id1", 20),
    ]

    assert calculate_credibility_score(records) == 30
