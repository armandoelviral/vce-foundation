from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.isk_isolation_preconditions import (
    IsolationPreconditions,
    PreconditionCheck,
    PreconditionStatus,
)


def check(**changes):
    values = {
        "check_id": "CHECK-001",
        "status": PreconditionStatus.SATISFIED,
        "evidence_ids": ("EVIDENCE-001",),
    }
    values.update(changes)
    return PreconditionCheck(**values)


def test_all_states_are_distinct():
    assert len(set(PreconditionStatus)) == 3


@pytest.mark.parametrize(
    "status",
    [PreconditionStatus.SATISFIED, PreconditionStatus.FAILED],
)
def test_resolved_states_require_evidence(status):
    with pytest.raises(ValueError):
        check(status=status, evidence_ids=())


def test_unknown_may_have_no_evidence():
    assert check(
        status=PreconditionStatus.UNKNOWN,
        evidence_ids=(),
    ).evidence_ids == ()


@pytest.mark.parametrize("invalid", ["", " ", None, 42])
def test_invalid_check_identity_is_rejected(invalid):
    with pytest.raises(ValueError):
        check(check_id=invalid)


@pytest.mark.parametrize("invalid", ["SATISFIED", None, 1])
def test_invalid_status_is_rejected(invalid):
    with pytest.raises(TypeError):
        check(status=invalid)


@pytest.mark.parametrize(
    "invalid",
    [[], ("",), (" ",), (None,), (1,), ("E-1", "E-1")],
)
def test_invalid_evidence_references_are_rejected(invalid):
    with pytest.raises((TypeError, ValueError)):
        check(evidence_ids=invalid)


def test_preconditions_require_checks():
    with pytest.raises(ValueError):
        IsolationPreconditions("EXP-001", ())


def test_duplicate_checks_are_rejected():
    with pytest.raises(ValueError):
        IsolationPreconditions(
            "EXP-001",
            (check(), replace(check(), status=PreconditionStatus.FAILED)),
        )


def test_invalid_check_type_is_rejected():
    with pytest.raises(TypeError):
        IsolationPreconditions("EXP-001", (object(),))


def test_preconditions_preserve_experiment_identity():
    record = IsolationPreconditions("EXP-001", (check(),))
    assert record.experiment_id == "EXP-001"


def test_records_are_immutable():
    record = IsolationPreconditions("EXP-001", (check(),))
    with pytest.raises(FrozenInstanceError):
        record.experiment_id = "EXP-002"
