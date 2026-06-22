from phase4.admission_policy_layer.reputation_requirement import (
    ReputationRequirement,
)


def test_contains_minimum_score():

    requirement = ReputationRequirement(
        minimum_score=100,
    )

    assert requirement.minimum_score == 100


def test_passes_when_score_is_enough():

    requirement = ReputationRequirement(
        minimum_score=100,
    )

    assert (
        requirement.is_satisfied(
            reputation_score=120,
        )
        is True
    )


def test_fails_when_score_is_too_low():

    requirement = ReputationRequirement(
        minimum_score=100,
    )

    assert (
        requirement.is_satisfied(
            reputation_score=80,
        )
        is False
    )


def test_serializes():

    requirement = ReputationRequirement(
        minimum_score=100,
    )

    assert requirement.to_dict() == {
        "requirement_type": "REPUTATION",
        "minimum_score": 100,
    }
