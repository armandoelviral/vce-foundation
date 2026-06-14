from epics.ztc25_formal_verification_certification.safety_property_validator import (
    SafetyPropertyValidator,
)


def test_accepts_satisfied_property():

    validator = SafetyPropertyValidator()

    assert validator.validate(
        property_satisfied=True,
    )


def test_rejects_violated_property():

    validator = SafetyPropertyValidator()

    assert not validator.validate(
        property_satisfied=False,
    )


def test_returns_boolean():

    validator = SafetyPropertyValidator()

    result = validator.validate(
        property_satisfied=True,
    )

    assert isinstance(
        result,
        bool,
    )
