from phase4.constitutional_obligations_layer.duty_violation import (
    DutyViolation,
)


def test_contains_duty_id():

    violation = DutyViolation(
        duty_id="duty-001",
        violation_type="response_invalidity",
    )

    assert violation.duty_id == "duty-001"


def test_contains_violation_type():

    violation = DutyViolation(
        duty_id="duty-001",
        violation_type="response_invalidity",
    )

    assert violation.violation_type == "response_invalidity"


def test_serializes():

    violation = DutyViolation(
        duty_id="duty-001",
        violation_type="response_invalidity",
    )

    assert violation.to_dict() == {
        "duty_id": "duty-001",
        "violation_type": "response_invalidity",
    }
