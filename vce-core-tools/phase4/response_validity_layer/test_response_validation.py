from phase4.response_validity_layer.response_validation import (
    ResponseValidation,
)


def test_valid_response():

    validation = ResponseValidation(
        citizen_did="did:tcn:test:01",
        response_valid=True,
    )

    assert validation.response_valid is True


def test_contains_did():

    validation = ResponseValidation(
        citizen_did="did:tcn:test:01",
        response_valid=True,
    )

    assert validation.citizen_did == (
        "did:tcn:test:01"
    )


def test_serializes():

    validation = ResponseValidation(
        citizen_did="did:tcn:test:01",
        response_valid=True,
    )

    assert validation.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "response_valid": True,
    }
