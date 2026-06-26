from epics.phase9_007_constitutional_outcome.outcome_result import (
    outcome_successful,
)


def test_successful_outcome():
    assert outcome_successful("successful") is True


def test_unsuccessful_outcome():
    assert outcome_successful("failed") is False
