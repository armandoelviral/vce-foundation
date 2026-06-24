from epics.phase6_002_constitutional_reputation.reputation_record import (
    ReputationRecord,
)


def test_reputation_record_creation():
    record = ReputationRecord(
        reputation_id="rep.001",
        identity_id="identity.001",
        score_delta=10,
    )

    assert record.reputation_id == "rep.001"


def test_requires_reputation_id():
    try:
        ReputationRecord(
            "",
            "identity.001",
            10,
        )
        assert False
    except ValueError as exc:
        assert "reputation_id" in str(exc)


def test_requires_identity_id():
    try:
        ReputationRecord(
            "rep.001",
            "",
            10,
        )
        assert False
    except ValueError as exc:
        assert "identity_id" in str(exc)
