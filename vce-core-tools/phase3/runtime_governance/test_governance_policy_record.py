from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)


def test_policy_contains_id():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    assert policy.policy_id == "policy-001"


def test_policy_contains_name():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    assert policy.policy_name == "default_governance"


def test_policy_serializes():

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    assert policy.to_dict() == {
        "policy_id": "policy-001",
        "policy_name": "default_governance",
    }
