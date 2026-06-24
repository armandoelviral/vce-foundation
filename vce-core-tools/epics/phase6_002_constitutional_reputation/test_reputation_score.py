from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)
from epics.phase6_002_constitutional_reputation.reputation_score import (
    calculate_reputation_score,
)


def test_calculates_score():
    records = [
        ReputationRecord("r1", "id1", 10),
        ReputationRecord("r2", "id1", 20),
    ]

    result = calculate_reputation_score(records)

    assert result == 30


def test_empty_score():
    assert calculate_reputation_score([]) == 0
