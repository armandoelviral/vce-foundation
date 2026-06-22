from phase4.constitutional_rights_layer.rights_verifier import (
    RightsVerifier,
)


class MockState:

    def __init__(self, rights_state):
        self.rights_state = rights_state


def test_protected_state():

    state = MockState("PROTECTED")

    assert RightsVerifier.verify(state) is True


def test_restored_state():

    state = MockState("RESTORED")

    assert RightsVerifier.verify(state) is True


def test_violated_state():

    state = MockState("VIOLATED")

    assert RightsVerifier.verify(state) is False
