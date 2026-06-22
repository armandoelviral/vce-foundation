from phase4.response_validity_layer.response_validity_state import (
    ResponseValidityState,
)


def test_contains_did():

    state = ResponseValidityState(
        citizen_did="did:tcn:test:01",
        response_state="VALID",
    )

    assert state.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_state():

    state = ResponseValidityState(
        citizen_did="did:tcn:test:01",
        response_state="VALID",
    )

    assert state.response_state == (
        "VALID"
    )


def test_serializes():

    state = ResponseValidityState(
        citizen_did="did:tcn:test:01",
        response_state="VALID",
    )

    assert state.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "response_state": "VALID",
    }
