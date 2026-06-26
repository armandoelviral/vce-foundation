from epics.phase9_006_constitutional_execution.execution_result import (
    execution_completed,
)


def test_execution_completed():
    assert execution_completed("completed") is True


def test_execution_not_completed():
    assert execution_completed("pending") is False
