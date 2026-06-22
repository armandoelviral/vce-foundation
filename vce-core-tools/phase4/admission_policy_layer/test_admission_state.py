from phase4.admission_policy_layer.admission_state import (
    AdmissionState,
)


def test_contains_did():

    state = AdmissionState(
        citizen_did="did:tcn:test:01",
        admission_state="ADMITTED",
    )

    assert state.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_state():

    state = AdmissionState(
        citizen_did="did:tcn:test:01",
        admission_state="ADMITTED",
    )

    assert state.admission_state == (
        "ADMITTED"
    )


def test_serializes():

    state = AdmissionState(
        citizen_did="did:tcn:test:01",
        admission_state="ADMITTED",
    )

    assert state.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "admission_state":
            "ADMITTED",
    }
