from phase4.admission_policy_layer.admission_requirement import (
    AdmissionRequirement,
)


def test_contains_requirement_name():

    requirement = AdmissionRequirement(
        requirement_name="minimum_reputation",
        requirement_value=100,
    )

    assert (
        requirement.requirement_name
        == "minimum_reputation"
    )


def test_contains_requirement_value():

    requirement = AdmissionRequirement(
        requirement_name="minimum_reputation",
        requirement_value=100,
    )

    assert (
        requirement.requirement_value
        == 100
    )


def test_serializes():

    requirement = AdmissionRequirement(
        requirement_name="minimum_reputation",
        requirement_value=100,
    )

    assert requirement.to_dict() == {
        "requirement_name":
            "minimum_reputation",
        "requirement_value":
            100,
    }
