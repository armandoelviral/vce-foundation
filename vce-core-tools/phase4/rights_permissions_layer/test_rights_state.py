from phase4.rights_permissions_layer.rights_state import (
    RightsState,
)


def test_contains_did():

    state = RightsState(
        citizen_did="did:tcn:test:01",
        rights_state="ACTIVE",
    )

    assert state.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_state():

    state = RightsState(
        citizen_did="did:tcn:test:01",
        rights_state="ACTIVE",
    )

    assert state.rights_state == (
        "ACTIVE"
    )


def test_serializes():

    state = RightsState(
        citizen_did="did:tcn:test:01",
        rights_state="ACTIVE",
    )

    assert state.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "rights_state":
            "ACTIVE",
    }
