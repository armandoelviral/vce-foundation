from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)
from epics.phase9_001_shared_intent.shared_intent_registry import (
    SharedIntentRegistry,
)


def test_registry_adds_shared_intent():
    registry = SharedIntentRegistry()

    record = SharedIntentRecord(
        "intent.001",
        "Preserve evidence",
        5,
    )

    registry.add(record)

    assert registry.records() == [record]
