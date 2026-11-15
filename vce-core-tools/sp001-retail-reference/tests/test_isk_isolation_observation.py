from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.isk_isolation_observation import (
    IsolationAttemptResult,
    IsolationObservation,
    PersistentEffectStatus,
)


def observation(**changes):
    values = {
        "observation_id": "OBS-001",
        "experiment_id": "EXP-001",
        "attempt_id": "RT-01",
        "os_result": IsolationAttemptResult.DENIED,
        "persistent_effect": PersistentEffectStatus.UNCHANGED,
        "evidence_ids": ("EVIDENCE-001",),
    }
    values.update(changes)
    return IsolationObservation(**values)


@pytest.mark.parametrize(
    "field",
    ["observation_id", "experiment_id", "attempt_id"],
)
@pytest.mark.parametrize("invalid", ["", " ", None, 42])
def test_invalid_identity_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        observation(**{field: invalid})


@pytest.mark.parametrize("invalid", ["DENIED", None, 1])
def test_invalid_attempt_result_is_rejected(invalid):
    with pytest.raises(TypeError):
        observation(os_result=invalid)


@pytest.mark.parametrize("invalid", ["UNCHANGED", None, 1])
def test_invalid_persistent_effect_is_rejected(invalid):
    with pytest.raises(TypeError):
        observation(persistent_effect=invalid)


@pytest.mark.parametrize(
    "invalid",
    [[], ("",), (" ",), (None,), (1,), ("E-1", "E-1")],
)
def test_invalid_evidence_references_are_rejected(invalid):
    with pytest.raises((TypeError, ValueError)):
        observation(evidence_ids=invalid)


@pytest.mark.parametrize(
    "os_result,persistent_effect",
    [
        (IsolationAttemptResult.DENIED, PersistentEffectStatus.UNKNOWN),
        (IsolationAttemptResult.UNKNOWN, PersistentEffectStatus.CHANGED),
        (IsolationAttemptResult.COMPLETED, PersistentEffectStatus.UNCHANGED),
        (IsolationAttemptResult.ERROR, PersistentEffectStatus.UNKNOWN),
    ],
)
def test_partial_or_resolved_observation_requires_evidence(
    os_result, persistent_effect
):
    with pytest.raises(ValueError):
        observation(
            os_result=os_result,
            persistent_effect=persistent_effect,
            evidence_ids=(),
        )


def test_fully_unknown_observation_can_have_no_evidence():
    record = observation(
        os_result=IsolationAttemptResult.UNKNOWN,
        persistent_effect=PersistentEffectStatus.UNKNOWN,
        evidence_ids=(),
    )
    assert record.evidence_ids == ()


def test_denied_with_changed_effect_is_preserved():
    record = observation(
        os_result=IsolationAttemptResult.DENIED,
        persistent_effect=PersistentEffectStatus.CHANGED,
    )
    assert record.persistent_effect is PersistentEffectStatus.CHANGED


def test_records_are_immutable():
    record = observation()
    with pytest.raises(FrozenInstanceError):
        record.attempt_id = "RT-02"


def test_replace_preserves_original():
    original = observation()
    changed = replace(original, attempt_id="RT-02")

    assert original.attempt_id == "RT-01"
    assert changed.attempt_id == "RT-02"
    assert changed.experiment_id == original.experiment_id
