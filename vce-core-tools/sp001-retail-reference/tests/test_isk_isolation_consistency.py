from dataclasses import replace

import pytest

from sp001.contracts.isk_isolation_experiment import (
    IsolationExperiment,
    IsolationPlatform,
)
from sp001.contracts.isk_isolation_observation import (
    IsolationAttemptResult,
    IsolationObservation,
    PersistentEffectStatus,
)
from sp001.contracts.isk_isolation_preconditions import (
    IsolationPreconditions,
    PreconditionCheck,
    PreconditionStatus,
)
from sp001.contracts.isk_isolation_verdict import (
    IsolationVerdict,
    IsolationVerdictStatus,
)
from sp001.services.isk_isolation_consistency import (
    validate_isolation_consistency,
)


def records():
    experiment = IsolationExperiment(
        experiment_id="EXP-001",
        platform=IsolationPlatform.MACOS,
        invariant_id="ISK-INV-03",
        threat_model_id="SEC-ISO-001",
        resource_id="RESOURCE-001",
        attempt_id="RT-01",
    )

    preconditions = IsolationPreconditions(
        experiment_id="EXP-001",
        checks=(
            PreconditionCheck(
                check_id="CHECK-001",
                status=PreconditionStatus.SATISFIED,
                evidence_ids=("EVIDENCE-PRE",),
            ),
        ),
    )

    observation = IsolationObservation(
        observation_id="OBS-001",
        experiment_id="EXP-001",
        attempt_id="RT-01",
        os_result=IsolationAttemptResult.DENIED,
        persistent_effect=PersistentEffectStatus.UNCHANGED,
        evidence_ids=("EVIDENCE-OBS",),
    )

    verdict = IsolationVerdict(
        verdict_id="VER-001",
        experiment_id="EXP-001",
        status=IsolationVerdictStatus.OBSERVED_HOLD,
        observation_ids=("OBS-001",),
        evidence_ids=("EVIDENCE-OBS",),
    )

    return {
        "experiment": experiment,
        "preconditions": preconditions,
        "observations": (observation,),
        "verdict": verdict,
    }


def test_valid_composition_returns_none():
    assert validate_isolation_consistency(**records()) is None


@pytest.mark.parametrize(
    "field",
    ["experiment", "preconditions", "observations", "verdict"],
)
def test_invalid_top_level_types_are_rejected(field):
    values = records()
    values[field] = object()

    with pytest.raises(TypeError):
        validate_isolation_consistency(**values)


def test_preconditions_identity_mismatch_is_rejected():
    values = records()
    values["preconditions"] = replace(
        values["preconditions"],
        experiment_id="OTHER-EXP",
    )

    with pytest.raises(ValueError, match="preconditions experiment"):
        validate_isolation_consistency(**values)


def test_verdict_identity_mismatch_is_rejected():
    values = records()
    values["verdict"] = replace(
        values["verdict"],
        experiment_id="OTHER-EXP",
    )

    with pytest.raises(ValueError, match="verdict experiment"):
        validate_isolation_consistency(**values)


def test_observation_experiment_mismatch_is_rejected():
    values = records()
    values["observations"] = (
        replace(values["observations"][0], experiment_id="OTHER-EXP"),
    )

    with pytest.raises(ValueError, match="observation experiment"):
        validate_isolation_consistency(**values)


def test_observation_attempt_mismatch_is_rejected():
    values = records()
    values["observations"] = (
        replace(values["observations"][0], attempt_id="OTHER-RT"),
    )

    with pytest.raises(ValueError, match="observation attempt"):
        validate_isolation_consistency(**values)


def test_duplicate_observations_are_rejected():
    values = records()
    observation = values["observations"][0]
    values["observations"] = (observation, observation)

    with pytest.raises(ValueError, match="duplicate observation"):
        validate_isolation_consistency(**values)


def test_missing_verdict_reference_is_rejected():
    values = records()
    values["verdict"] = replace(
        values["verdict"],
        observation_ids=("OTHER-OBS",),
    )

    with pytest.raises(ValueError, match="observation references"):
        validate_isolation_consistency(**values)


def test_unreferenced_supplied_observation_is_rejected():
    values = records()
    additional = replace(
        values["observations"][0],
        observation_id="OBS-002",
    )
    values["observations"] += (additional,)

    with pytest.raises(ValueError, match="observation references"):
        validate_isolation_consistency(**values)


def test_not_tested_without_observations_is_consistent():
    values = records()
    values["observations"] = ()
    values["verdict"] = replace(
        values["verdict"],
        status=IsolationVerdictStatus.NOT_TESTED,
        observation_ids=(),
    )

    assert validate_isolation_consistency(**values) is None


def test_indeterminate_without_observations_is_consistent():
    values = records()
    values["observations"] = ()
    values["verdict"] = replace(
        values["verdict"],
        status=IsolationVerdictStatus.INDETERMINATE,
        observation_ids=(),
    )

    assert validate_isolation_consistency(**values) is None


def test_external_evidence_reference_is_preserved():
    values = records()
    values["verdict"] = replace(
        values["verdict"],
        evidence_ids=("EVIDENCE-OBS", "EXTERNAL-EVIDENCE"),
    )

    assert validate_isolation_consistency(**values) is None
    assert values["verdict"].evidence_ids == (
        "EVIDENCE-OBS",
        "EXTERNAL-EVIDENCE",
    )
