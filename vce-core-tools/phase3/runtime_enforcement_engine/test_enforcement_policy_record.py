from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)


def test_policy_contains_id():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    assert policy.policy_id == "policy-001"


def test_policy_contains_name():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    assert policy.policy_name == "default_enforcement"


def test_policy_serializes():

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    assert policy.to_dict() == {
        "policy_id": "policy-001",
        "policy_name": "default_enforcement",
    }
