from phase4.response_validity_layer.response_failure_record import (
    ResponseFailureRecord,
)


def test_contains_did():

    record = ResponseFailureRecord(
        citizen_did="did:tcn:test:01",
        failure_reason="response_invalidity",
    )

    assert record.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_reason():

    record = ResponseFailureRecord(
        citizen_did="did:tcn:test:01",
        failure_reason="response_invalidity",
    )

    assert record.failure_reason == (
        "response_invalidity"
    )


def test_serializes():

    record = ResponseFailureRecord(
        citizen_did="did:tcn:test:01",
        failure_reason="response_invalidity",
    )

    assert record.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "failure_reason":
            "response_invalidity",
        "recorded": True,
    }
