from phase4.constitutional_obligations_layer.duty_verifier import (
    DutyVerifier,
)


class MockState:

    def __init__(self, duty_state):
        self.duty_state = duty_state


def test_compliant_state():

    state = MockState("COMPLIANT")

    assert DutyVerifier.verify(state) is True


def test_restored_state():

    state = MockState("RESTORED")

    assert DutyVerifier.verify(state) is True


def test_violated_state():

    state = MockState("VIOLATED")

    assert DutyVerifier.verify(state) is False
