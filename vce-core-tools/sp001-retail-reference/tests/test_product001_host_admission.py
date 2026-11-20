
from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.isk_isolation_preconditions import (
    IsolationPreconditions,
    PreconditionCheck,
    PreconditionStatus,
)
from sp001.contracts.product001_host_admission import (
    HostAdmissionStatus,
    assess_product001_host_admission,
)


def preconditions(overrides=None, missing=(), extra=()):
    overrides = overrides or {}

    checks = [
        PreconditionCheck(
            check_id=f"HOST-P{i:02d}",
            status=overrides.get(
                f"HOST-P{i:02d}",
                PreconditionStatus.SATISFIED,
            ),
            evidence_ids=(f"EVIDENCE-{i:02d}",),
        )
        for i in range(1, 11)
        if f"HOST-P{i:02d}" not in missing
    ]

    checks.extend(extra)

    return IsolationPreconditions(
        experiment_id="HOST-B1-D1A",
        checks=tuple(checks),
    )


def test_all_satisfied_is_eligible():
    result = assess_product001_host_admission(
        preconditions()
    )

    assert result.status is HostAdmissionStatus.ELIGIBLE
    assert result.failed_check_ids == ()
    assert result.unknown_check_ids == ()


def test_failed_precondition_is_rejected():
    result = assess_product001_host_admission(
        preconditions({
            "HOST-P03": PreconditionStatus.FAILED
        })
    )

    assert result.status is HostAdmissionStatus.REJECTED
    assert result.failed_check_ids == ("HOST-P03",)


def test_unknown_precondition_is_indeterminate():
    result = assess_product001_host_admission(
        preconditions({
            "HOST-P04": PreconditionStatus.UNKNOWN
        })
    )

    assert result.status is HostAdmissionStatus.INDETERMINATE
    assert result.unknown_check_ids == ("HOST-P04",)


def test_failure_precedes_unknown():
    result = assess_product001_host_admission(
        preconditions({
            "HOST-P03": PreconditionStatus.FAILED,
            "HOST-P04": PreconditionStatus.UNKNOWN,
        })
    )

    assert result.status is HostAdmissionStatus.REJECTED
    assert result.failed_check_ids == ("HOST-P03",)
    assert result.unknown_check_ids == ("HOST-P04",)


def test_missing_required_check_is_rejected():
    with pytest.raises(
        ValueError,
        match="coverage mismatch",
    ):
        assess_product001_host_admission(
            preconditions(missing=("HOST-P10",))
        )


def test_extra_check_is_rejected():
    extra = PreconditionCheck(
        check_id="HOST-P11",
        status=PreconditionStatus.SATISFIED,
        evidence_ids=("EVIDENCE-11",),
    )

    with pytest.raises(
        ValueError,
        match="coverage mismatch",
    ):
        assess_product001_host_admission(
            preconditions(extra=(extra,))
        )


def test_invalid_argument_type_is_rejected():
    with pytest.raises(TypeError):
        assess_product001_host_admission(None)


def test_input_is_not_mutated():
    original = preconditions()

    before = original.checks

    assess_product001_host_admission(original)

    assert original.checks == before
    assert original.checks is before


def test_assessment_is_immutable():
    result = assess_product001_host_admission(
        preconditions()
    )

    with pytest.raises(FrozenInstanceError):
        result.status = HostAdmissionStatus.REJECTED
