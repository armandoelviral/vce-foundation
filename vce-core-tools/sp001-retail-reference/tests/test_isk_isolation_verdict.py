from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.isk_isolation_verdict import (
    IsolationVerdict,
    IsolationVerdictStatus,
)


def verdict(**changes):
    values = {
        "verdict_id": "VER-001",
        "experiment_id": "EXP-001",
        "status": IsolationVerdictStatus.OBSERVED_HOLD,
        "observation_ids": ("OBS-001",),
        "evidence_ids": ("EVIDENCE-001",),
    }
    values.update(changes)
    return IsolationVerdict(**values)


@pytest.mark.parametrize(
    "status",
    list(IsolationVerdictStatus),
)
def test_all_declared_statuses_are_accepted(status):
    changes = {"status": status}

    if status is IsolationVerdictStatus.NOT_TESTED:
        changes["observation_ids"] = ()

    assert verdict(**changes).status is status


@pytest.mark.parametrize("field", ["verdict_id", "experiment_id"])
@pytest.mark.parametrize("invalid", ["", " ", None, 42])
def test_invalid_identity_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        verdict(**{field: invalid})


@pytest.mark.parametrize("invalid", ["FALSIFIED", None, 1])
def test_invalid_status_is_rejected(invalid):
    with pytest.raises(TypeError):
        verdict(status=invalid)


@pytest.mark.parametrize(
    "field",
    ["observation_ids", "evidence_ids"],
)
@pytest.mark.parametrize(
    "invalid",
    [[], ("",), (" ",), (None,), (1,), ("ID-1", "ID-1")],
)
def test_invalid_references_are_rejected(field, invalid):
    with pytest.raises((TypeError, ValueError)):
        verdict(**{field: invalid})


@pytest.mark.parametrize(
    "status",
    [
        IsolationVerdictStatus.OBSERVED_HOLD,
        IsolationVerdictStatus.FALSIFIED,
    ],
)
@pytest.mark.parametrize(
    "field",
    ["observation_ids", "evidence_ids"],
)
def test_conclusive_verdict_requires_references(status, field):
    with pytest.raises(ValueError):
        verdict(status=status, **{field: ()})


def test_indeterminate_can_preserve_partial_evidence():
    record = verdict(
        status=IsolationVerdictStatus.INDETERMINATE,
        observation_ids=(),
    )
    assert record.evidence_ids == ("EVIDENCE-001",)


def test_indeterminate_can_have_no_evidence():
    record = verdict(
        status=IsolationVerdictStatus.INDETERMINATE,
        observation_ids=(),
        evidence_ids=(),
    )
    assert record.status is IsolationVerdictStatus.INDETERMINATE


def test_not_tested_rejects_observations():
    with pytest.raises(ValueError):
        verdict(status=IsolationVerdictStatus.NOT_TESTED)


def test_not_tested_can_preserve_explanatory_evidence():
    record = verdict(
        status=IsolationVerdictStatus.NOT_TESTED,
        observation_ids=(),
    )
    assert record.evidence_ids == ("EVIDENCE-001",)


def test_verdict_is_immutable():
    record = verdict()

    with pytest.raises(FrozenInstanceError):
        record.status = IsolationVerdictStatus.FALSIFIED


def test_replace_preserves_original():
    original = verdict()
    changed = replace(
        original,
        status=IsolationVerdictStatus.FALSIFIED,
    )

    assert original.status is IsolationVerdictStatus.OBSERVED_HOLD
    assert changed.status is IsolationVerdictStatus.FALSIFIED
    assert changed.experiment_id == original.experiment_id
