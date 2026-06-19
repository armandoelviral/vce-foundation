from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)


def test_policy_contains_id():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    assert policy.policy_id == "policy-001"


def test_policy_contains_name():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    assert policy.policy_name == "default_trust"


def test_policy_serializes():

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    assert policy.to_dict() == {
        "policy_id": "policy-001",
        "policy_name": "default_trust",
    }
