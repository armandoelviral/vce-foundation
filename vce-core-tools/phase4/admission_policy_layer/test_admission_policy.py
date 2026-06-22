from phase4.admission_policy_layer.admission_policy import (
    AdmissionPolicy,
)


def test_contains_policy_name():

    policy = AdmissionPolicy(
        policy_name="citizen_admission_policy",
        requirements=[
            "minimum_reputation",
            "response_validity",
        ],
    )

    assert (
        policy.policy_name
        == "citizen_admission_policy"
    )


def test_contains_requirements():

    policy = AdmissionPolicy(
        policy_name="citizen_admission_policy",
        requirements=[
            "minimum_reputation",
            "response_validity",
        ],
    )

    assert len(
        policy.requirements
    ) == 2


def test_serializes():

    policy = AdmissionPolicy(
        policy_name="citizen_admission_policy",
        requirements=[
            "minimum_reputation",
            "response_validity",
        ],
    )

    assert policy.to_dict() == {
        "policy_name":
            "citizen_admission_policy",
        "requirements": [
            "minimum_reputation",
            "response_validity",
        ],
    }
