from phase4.reputation_layer.reputation_recovery import (
    ReputationRecovery,
)


def test_contains_did():

    recovery = ReputationRecovery(
        citizen_did="did:tcn:test:01",
        recovery_reason="sustained_valid_response",
        recovery_points=15,
    )

    assert recovery.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_reason():

    recovery = ReputationRecovery(
        citizen_did="did:tcn:test:01",
        recovery_reason="sustained_valid_response",
        recovery_points=15,
    )

    assert recovery.recovery_reason == (
        "sustained_valid_response"
    )


def test_contains_points():

    recovery = ReputationRecovery(
        citizen_did="did:tcn:test:01",
        recovery_reason="sustained_valid_response",
        recovery_points=15,
    )

    assert recovery.recovery_points == 15


def test_serializes():

    recovery = ReputationRecovery(
        citizen_did="did:tcn:test:01",
        recovery_reason="sustained_valid_response",
        recovery_points=15,
    )

    assert recovery.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "recovery_reason":
            "sustained_valid_response",
        "recovery_points":
            15,
    }
