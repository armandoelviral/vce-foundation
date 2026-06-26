from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)


def test_shared_intent_creation():
    record = SharedIntentRecord(
        intent_id="intent.001",
        purpose="Preserve evidence",
        participants=5,
    )

    assert record.intent_id == "intent.001"
    assert record.participants == 5


def test_requires_intent_id():
    try:
        SharedIntentRecord(
            "",
            "Preserve evidence",
            5,
        )
        assert False
    except ValueError as exc:
        assert "intent_id" in str(exc)
