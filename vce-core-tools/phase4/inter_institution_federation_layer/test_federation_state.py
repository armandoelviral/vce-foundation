from phase4.inter_institution_federation_layer.federation_state import (
    FederationState,
)


def test_contains_state():

    state = FederationState(
        federation_state="HEALTHY",
    )

    assert (
        state.federation_state
        == "HEALTHY"
    )


def test_serializes():

    state = FederationState(
        federation_state="HEALTHY",
    )

    assert state.to_dict() == {
        "federation_state":
            "HEALTHY",
    }


def test_disputed_state():

    state = FederationState(
        federation_state="DISPUTED",
    )

    assert (
        state.federation_state
        == "DISPUTED"
    )
