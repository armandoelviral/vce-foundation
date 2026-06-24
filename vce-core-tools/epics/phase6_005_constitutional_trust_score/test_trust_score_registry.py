from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)
from epics.phase6_005_constitutional_trust_score.trust_score_registry import (
    TrustScoreRegistry,
)


def test_registry_adds_score():
    registry = TrustScoreRegistry()

    record = TrustScoreRecord(
        "score.001",
        "identity.001",
        75,
    )

    registry.add(record)

    assert registry.records() == [record]
