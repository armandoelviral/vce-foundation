from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)


def test_learning_record_creation():
    record = LearningRecord(
        learning_id="learning.001",
        outcome_id="outcome.001",
        lesson="Replay policy improved audit quality",
    )

    assert record.learning_id == "learning.001"
    assert record.outcome_id == "outcome.001"


def test_requires_learning_id():
    try:
        LearningRecord(
            "",
            "outcome.001",
            "Lesson",
        )
        assert False
    except ValueError as exc:
        assert "learning_id" in str(exc)
