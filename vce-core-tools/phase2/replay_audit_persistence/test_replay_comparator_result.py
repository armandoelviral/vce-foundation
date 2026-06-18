from phase2.replay_audit_persistence.replay_comparator_result import (
    ReplayComparatorResult,
)


def test_result_contains_expected_hash():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    assert (
        result.expected_hash
        == "hash-001"
    )


def test_result_contains_actual_hash():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    assert (
        result.actual_hash
        == "hash-001"
    )


def test_result_contains_match_status():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    assert result.match is True


def test_result_serializes():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    assert result.to_dict() == {
        "expected_hash": "hash-001",
        "actual_hash": "hash-001",
        "match": True,
    }
