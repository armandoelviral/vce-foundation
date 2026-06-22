from phase4.policy_enforcement_layer.policy_violation import (
    PolicyViolation,
)


def test_contains_policy_id():

    violation = PolicyViolation(
        policy_id="policy-001",
        violation_type=(
            "minimum_reputation_not_met"
        ),
    )

    assert (
        violation.policy_id
        == "policy-001"
    )


def test_contains_violation_type():

    violation = PolicyViolation(
        policy_id="policy-001",
        violation_type=(
            "minimum_reputation_not_met"
        ),
    )

    assert (
        violation.violation_type
        == "minimum_reputation_not_met"
    )


def test_serializes():

    violation = PolicyViolation(
        policy_id="policy-001",
        violation_type=(
            "minimum_reputation_not_met"
        ),
    )

    assert violation.to_dict() == {
        "policy_id":
            "policy-001",
        "violation_type":
            "minimum_reputation_not_met",
    }
