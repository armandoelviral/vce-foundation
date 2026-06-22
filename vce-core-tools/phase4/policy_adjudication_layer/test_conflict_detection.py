from phase4.policy_adjudication_layer.conflict_detection import (
    ConflictDetection,
)


def test_detects_conflict():

    result = ConflictDetection.detect(
        policy_a="minimum_reputation_100",
        policy_b="minimum_reputation_200",
    )

    assert result["conflict"] is True


def test_no_conflict_when_same_policy():

    result = ConflictDetection.detect(
        policy_a="minimum_reputation_100",
        policy_b="minimum_reputation_100",
    )

    assert result["conflict"] is False


def test_serializes_conflict_result():

    result = ConflictDetection.detect(
        policy_a="minimum_reputation_100",
        policy_b="minimum_reputation_200",
    )

    assert result == {
        "policy_a": "minimum_reputation_100",
        "policy_b": "minimum_reputation_200",
        "conflict": True,
    }
