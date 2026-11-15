from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.isk_isolation_experiment import (
    IsolationExperiment,
    IsolationPlatform,
)


def experiment(**changes):
    values = {
        "experiment_id": "EXP-001",
        "platform": IsolationPlatform.MACOS,
        "invariant_id": "ISK-INV-03",
        "threat_model_id": "SEC-ISO-001",
        "resource_id": "RESOURCE-001",
        "attempt_id": "RT-01",
    }
    values.update(changes)
    return IsolationExperiment(**values)


@pytest.mark.parametrize(
    "platform",
    [IsolationPlatform.MACOS, IsolationPlatform.LINUX],
)
def test_supported_platforms(platform):
    assert experiment(platform=platform).platform is platform


@pytest.mark.parametrize(
    "field",
    [
        "experiment_id",
        "invariant_id",
        "threat_model_id",
        "resource_id",
        "attempt_id",
    ],
)
@pytest.mark.parametrize("invalid", ["", "   ", None, 42])
def test_invalid_identity_is_rejected(field, invalid):
    with pytest.raises(ValueError):
        experiment(**{field: invalid})


@pytest.mark.parametrize("invalid", ["MACOS", "WINDOWS", None, 1])
def test_invalid_platform_is_rejected(invalid):
    with pytest.raises(TypeError):
        experiment(platform=invalid)


def test_experiment_is_immutable():
    record = experiment()

    with pytest.raises(FrozenInstanceError):
        record.experiment_id = "OTHER"


def test_dynamic_attributes_are_rejected():
    record = experiment()

    with pytest.raises((AttributeError, TypeError)):
        record.unexpected = "value"


def test_replace_preserves_unmodified_fields():
    original = experiment()
    changed = replace(original, attempt_id="RT-02")

    assert changed.attempt_id == "RT-02"
    assert changed.experiment_id == original.experiment_id
    assert changed.platform is original.platform
    assert original.attempt_id == "RT-01"
