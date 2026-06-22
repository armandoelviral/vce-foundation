from phase4.constitutional_evolution_layer.constitution_state import (
    ConstitutionState,
)


def test_contains_state():

    state = ConstitutionState(
        constitution_state="ACTIVE",
    )

    assert state.constitution_state == "ACTIVE"


def test_serializes():

    state = ConstitutionState(
        constitution_state="ACTIVE",
    )

    assert state.to_dict() == {
        "constitution_state": "ACTIVE",
    }


def test_supports_amended_state():

    state = ConstitutionState(
        constitution_state="AMENDED",
    )

    assert state.constitution_state == "AMENDED"
