from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)


def test_trust_score_record_creation():
    record = TrustScoreRecord(
        score_id="score.001",
        identity_id="identity.001",
        score=75,
    )

    assert record.score == 75


def test_requires_score_id():
    try:
        TrustScoreRecord(
            "",
            "identity.001",
            75,
        )
        assert False
    except ValueError as exc:
        assert "score_id" in str(exc)
