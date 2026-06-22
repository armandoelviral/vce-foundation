from phase4.admission_policy_layer.eligibility_evaluation import (
    EligibilityEvaluation,
)


def test_contains_did():

    evaluation = EligibilityEvaluation(
        citizen_did="did:tcn:test:01",
        eligible=True,
    )

    assert evaluation.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_eligibility():

    evaluation = EligibilityEvaluation(
        citizen_did="did:tcn:test:01",
        eligible=True,
    )

    assert evaluation.eligible is True


def test_serializes():

    evaluation = EligibilityEvaluation(
        citizen_did="did:tcn:test:01",
        eligible=True,
    )

    assert evaluation.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "eligible":
            True,
    }
