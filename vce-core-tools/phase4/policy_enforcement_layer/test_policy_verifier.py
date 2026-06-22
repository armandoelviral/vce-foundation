from phase4.policy_enforcement_layer.policy_verifier import (
    PolicyVerifier,
)


class MockState:

    def __init__(self, policy_state):
        self.policy_state = policy_state


def test_active_policy():

    state = MockState(
        "ACTIVE",
    )

    assert (
        PolicyVerifier.verify(
            state
        )
        is True
    )


def test_enforced_policy():

    state = MockState(
        "ENFORCED",
    )

    assert (
        PolicyVerifier.verify(
            state
        )
        is True
    )


def test_violated_policy():

    state = MockState(
        "VIOLATED",
    )

    assert (
        PolicyVerifier.verify(
            state
        )
        is False
    )
