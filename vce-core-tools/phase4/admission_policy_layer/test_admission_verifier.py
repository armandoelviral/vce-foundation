from phase4.admission_policy_layer.admission_verifier import (
    AdmissionVerifier,
)


class MockState:

    def __init__(
        self,
        admission_state,
    ):
        self.admission_state = (
            admission_state
        )


def test_admitted_state():

    state = MockState(
        "ADMITTED",
    )

    assert (
        AdmissionVerifier.verify(
            state
        )
        is True
    )


def test_pending_state():

    state = MockState(
        "PENDING",
    )

    assert (
        AdmissionVerifier.verify(
            state
        )
        is False
    )


def test_denied_state():

    state = MockState(
        "DENIED",
    )

    assert (
        AdmissionVerifier.verify(
            state
        )
        is False
    )
