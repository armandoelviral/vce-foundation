from phase4.constitutional_obligations_layer.duty_compliance import (
    DutyCompliance,
)


def test_contains_duty_id():

    compliance = DutyCompliance(
        duty_id="duty-001",
        compliant=True,
    )

    assert compliance.duty_id == "duty-001"


def test_contains_compliance():

    compliance = DutyCompliance(
        duty_id="duty-001",
        compliant=True,
    )

    assert compliance.compliant is True


def test_serializes():

    compliance = DutyCompliance(
        duty_id="duty-001",
        compliant=True,
    )

    assert compliance.to_dict() == {
        "duty_id": "duty-001",
        "compliant": True,
    }
