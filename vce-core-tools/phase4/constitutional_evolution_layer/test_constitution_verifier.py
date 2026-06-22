from phase4.constitutional_evolution_layer.constitution_verifier import (
    ConstitutionVerifier,
)


class MockState:

    def __init__(self, constitution_state):
        self.constitution_state = constitution_state


def test_active_state():

    state = MockState("ACTIVE")

    assert ConstitutionVerifier.verify(state) is True


def test_amended_state():

    state = MockState("AMENDED")

    assert ConstitutionVerifier.verify(state) is True


def test_suspended_state():

    state = MockState("SUSPENDED")

    assert ConstitutionVerifier.verify(state) is False
