from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)


def test_policy_contains_id():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    assert policy.policy_id == "policy-001"


def test_policy_contains_name():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    assert policy.policy_name == "default_admission"


def test_policy_serializes():

    policy = AdmissionPolicyRecord(
        policy_id="policy-001",
        policy_name="default_admission",
    )

    assert policy.to_dict() == {
        "policy_id": "policy-001",
        "policy_name": "default_admission",
    }
