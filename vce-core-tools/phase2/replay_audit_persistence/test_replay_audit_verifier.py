from phase2.replay_audit_persistence.replay_comparator_result import (
    ReplayComparatorResult,
)

from phase2.replay_audit_persistence.replay_audit_verifier import (
    ReplayAuditVerifier,
)


def test_verifier_accepts_matching_result():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=True,
    )

    assert (
        ReplayAuditVerifier.verify(
            result
        )
        is True
    )


def test_verifier_rejects_mismatch():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-999",
        match=False,
    )

    assert (
        ReplayAuditVerifier.verify(
            result
        )
        is False
    )


def test_verifier_rejects_false_match_flag():

    result = ReplayComparatorResult(
        expected_hash="hash-001",
        actual_hash="hash-001",
        match=False,
    )

    assert (
        ReplayAuditVerifier.verify(
            result
        )
        is False
    )
