from phase4.response_validity_layer.response_recovery_record import (
    ResponseRecoveryRecord,
)


def test_contains_did():

    record = ResponseRecoveryRecord(
        citizen_did="did:tcn:test:01",
        recovery_reason="response_capability_restored",
    )

    assert record.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_reason():

    record = ResponseRecoveryRecord(
        citizen_did="did:tcn:test:01",
        recovery_reason="response_capability_restored",
    )

    assert record.recovery_reason == (
        "response_capability_restored"
    )


def test_serializes():

    record = ResponseRecoveryRecord(
        citizen_did="did:tcn:test:01",
        recovery_reason="response_capability_restored",
    )

    assert record.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "recovery_reason":
            "response_capability_restored",
        "recorded":
            True,
    }
