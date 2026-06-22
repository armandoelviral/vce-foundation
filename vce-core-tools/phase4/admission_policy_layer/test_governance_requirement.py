from phase4.admission_policy_layer.governance_requirement import (
    GovernanceRequirement,
)


def test_accepts_active():

    requirement = GovernanceRequirement()

    assert (
        requirement.is_satisfied(
            governance_state="ACTIVE",
        )
        is True
    )


def test_rejects_suspended():

    requirement = GovernanceRequirement()

    assert (
        requirement.is_satisfied(
            governance_state="SUSPENDED",
        )
        is False
    )


def test_rejects_revoked():

    requirement = GovernanceRequirement()

    assert (
        requirement.is_satisfied(
            governance_state="REVOKED",
        )
        is False
    )


def test_serializes():

    requirement = GovernanceRequirement()

    assert requirement.to_dict() == {
        "requirement_type":
            "GOVERNANCE",
        "required_state":
            "ACTIVE",
    }
