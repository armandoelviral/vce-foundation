from epics.phase9_008_constitutional_learning.learning_capture import (
    learning_captured,
)


def test_learning_captured():
    assert learning_captured("Important lesson") is True


def test_learning_missing():
    assert learning_captured("") is False
