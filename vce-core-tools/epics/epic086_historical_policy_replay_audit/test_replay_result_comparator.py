from epics.epic086_historical_policy_replay_audit.replay_result_comparator import (
    ReplayResultComparator,
)


def test_comparator_accepts_matching_decisions():

    comparator = ReplayResultComparator()

    result = comparator.compare(
        original_decision="ADMIT",
        replay_decision="ADMIT",
    )

    assert result["result"] == "REPLAY_MATCH"


def test_comparator_rejects_mismatched_decisions():

    comparator = ReplayResultComparator()

    result = comparator.compare(
        original_decision="ADMIT",
        replay_decision="REJECT",
    )

    assert result["result"] == "REPLAY_MISMATCH"


def test_comparator_returns_original_and_replay_decisions():

    comparator = ReplayResultComparator()

    result = comparator.compare(
        original_decision="REJECT",
        replay_decision="ADMIT",
    )

    assert result["original_decision"] == "REJECT"
    assert result["replay_decision"] == "ADMIT"
