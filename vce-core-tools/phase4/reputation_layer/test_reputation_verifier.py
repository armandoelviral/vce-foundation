from phase4.reputation_layer.reputation_verifier import (
    ReputationVerifier,
)


class MockState:

    def __init__(
        self,
        reputation_state,
    ):
        self.reputation_state = (
            reputation_state
        )


def test_trusted_state():

    state = MockState(
        "TRUSTED",
    )

    assert (
        ReputationVerifier.verify(
            state
        )
        is True
    )


def test_recovering_state():

    state = MockState(
        "RECOVERING",
    )

    assert (
        ReputationVerifier.verify(
            state
        )
        is True
    )


def test_degraded_state():

    state = MockState(
        "DEGRADED",
    )

    assert (
        ReputationVerifier.verify(
            state
        )
        is False
    )
