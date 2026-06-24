from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)
from epics.phase6_005_constitutional_trust_score.trust_score_registry import (
    TrustScoreRegistry,
)
from epics.phase6_005_constitutional_trust_score.trust_score_state import (
    TrustScoreState,
)
from epics.phase6_005_constitutional_trust_score.trust_score_verifier import (
    verify_trust_score,
)


def test_end_to_end_trust_score_flow():
    registry = TrustScoreRegistry()

    registry.add(
        TrustScoreRecord(
            "score.001",
            "identity.001",
            75,
        )
    )

    registry.add(
        TrustScoreRecord(
            "score.002",
            "identity.001",
            85,
        )
    )

    state = TrustScoreState.from_records(
        registry.records()
    )

    verification = verify_trust_score(state)

    assert verification["verified"] is True
    assert verification["average_score"] == 80
