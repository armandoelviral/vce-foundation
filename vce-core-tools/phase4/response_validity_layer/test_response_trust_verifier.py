from phase4.response_validity_layer.response_trust_verifier import (
    ResponseTrustVerifier,
)


class MockState:

    def __init__(self, response_state):
        self.response_state = response_state


def test_valid_state():

    state = MockState("VALID")

    assert (
        ResponseTrustVerifier.verify(state)
        is True
    )


def test_invalid_state():

    state = MockState("INVALID")

    assert (
        ResponseTrustVerifier.verify(state)
        is False
    )


def test_recovered_state():

    state = MockState("RECOVERED")

    assert (
        ResponseTrustVerifier.verify(state)
        is True
    )
