from epics.phase9_004_constitutional_decision.decision_result import (
    decision_is_final,
)


def test_decision_is_final():
    assert decision_is_final("accepted") is True


def test_unknown_result_is_not_final():
    assert decision_is_final("pending") is False
