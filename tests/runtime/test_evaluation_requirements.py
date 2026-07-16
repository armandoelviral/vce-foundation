import pytest

from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)


def test_defaults_are_zero() -> None:
    requirements = EvaluationRequirements()

    assert requirements.minimum_evidence == 0
    assert requirements.minimum_independent_validations == 0
    assert requirements.minimum_destruction_attempts == 0


def test_accepts_custom_requirements() -> None:
    requirements = EvaluationRequirements(
        minimum_evidence=3,
        minimum_independent_validations=2,
        minimum_destruction_attempts=4,
    )

    assert requirements.minimum_evidence == 3
    assert requirements.minimum_independent_validations == 2
    assert requirements.minimum_destruction_attempts == 4


def test_rejects_negative_requirements() -> None:
    with pytest.raises(
        ValueError,
        match="evaluation requirements cannot be negative",
    ):
        EvaluationRequirements(minimum_evidence=-1)
