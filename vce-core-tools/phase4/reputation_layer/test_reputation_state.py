from phase4.reputation_layer.reputation_state import (
    ReputationState,
)


def test_contains_did():

    state = ReputationState(
        citizen_did="did:tcn:test:01",
        reputation_state="TRUSTED",
    )

    assert state.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_state():

    state = ReputationState(
        citizen_did="did:tcn:test:01",
        reputation_state="TRUSTED",
    )

    assert state.reputation_state == (
        "TRUSTED"
    )


def test_serializes():

    state = ReputationState(
        citizen_did="did:tcn:test:01",
        reputation_state="TRUSTED",
    )

    assert state.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "reputation_state":
            "TRUSTED",
    }
