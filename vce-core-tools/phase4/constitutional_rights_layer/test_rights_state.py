from phase4.constitutional_rights_layer.rights_state import (
    RightsState,
)


def test_contains_state():

    state = RightsState(
        rights_state="PROTECTED",
    )

    assert state.rights_state == "PROTECTED"


def test_serializes():

    state = RightsState(
        rights_state="PROTECTED",
    )

    assert state.to_dict() == {
        "rights_state": "PROTECTED",
    }


def test_violation_state():

    state = RightsState(
        rights_state="VIOLATED",
    )

    assert state.rights_state == "VIOLATED"
