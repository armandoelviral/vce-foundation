from phase4.constitutional_obligations_layer.duty_registry import (
    DutyRegistry,
)

from phase4.constitutional_obligations_layer.constitutional_duty import (
    ConstitutionalDuty,
)


def test_contains_duties():

    registry = DutyRegistry(
        duties=[
            ConstitutionalDuty(
                duty_id="duty-001",
                duty_name="maintain_response_validity",
            ),
        ]
    )

    assert len(registry.duties) == 1


def test_serializes():

    registry = DutyRegistry(
        duties=[
            ConstitutionalDuty(
                duty_id="duty-001",
                duty_name="maintain_response_validity",
            ),
        ]
    )

    assert registry.to_dict() == {
        "duties": [
            {
                "duty_id": "duty-001",
                "duty_name": "maintain_response_validity",
            }
        ]
    }
