from epics.phase9_001_shared_intent.shared_intent_alignment import (
    shared_intent_aligned,
)


def test_shared_intent_aligned():
    assert shared_intent_aligned(5, 5) is True


def test_shared_intent_not_aligned():
    assert shared_intent_aligned(5, 3) is False
