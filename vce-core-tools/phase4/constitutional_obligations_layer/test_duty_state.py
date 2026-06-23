from phase4.constitutional_obligations_layer.duty_state import (
    DutyState,
)


def test_contains_state():

    state = DutyState(
        duty_state="COMPLIANT",
    )

    assert state.duty_state == "COMPLIANT"


def test_serializes():

    state = DutyState(
        duty_state="COMPLIANT",
    )

    assert state.to_dict() == {
        "duty_state": "COMPLIANT",
    }


def test_violation_state():

    state = DutyState(
        duty_state="VIOLATED",
    )

    assert state.duty_state == "VIOLATED"
