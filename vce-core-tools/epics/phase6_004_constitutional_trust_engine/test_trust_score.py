from epics.phase6_004_constitutional_trust_engine.trust_record import (
    TrustRecord,
)
from epics.phase6_004_constitutional_trust_engine.trust_score import (
    calculate_trust_score,
)


def test_calculates_trust_score():
    records = [
        TrustRecord("t1", "id1", 10),
        TrustRecord("t2", "id1", 20),
    ]

    assert calculate_trust_score(records) == 30
