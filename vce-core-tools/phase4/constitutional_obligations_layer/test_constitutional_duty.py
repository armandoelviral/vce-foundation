from phase4.constitutional_obligations_layer.constitutional_duty import (
    ConstitutionalDuty,
)


def test_contains_duty_id():

    duty = ConstitutionalDuty(
        duty_id="duty-001",
        duty_name="maintain_response_validity",
    )

    assert duty.duty_id == "duty-001"


def test_contains_duty_name():

    duty = ConstitutionalDuty(
        duty_id="duty-001",
        duty_name="maintain_response_validity",
    )

    assert duty.duty_name == "maintain_response_validity"


def test_serializes():

    duty = ConstitutionalDuty(
        duty_id="duty-001",
        duty_name="maintain_response_validity",
    )

    assert duty.to_dict() == {
        "duty_id": "duty-001",
        "duty_name": "maintain_response_validity",
    }
