from phase4.response_validity_layer.response_capability import (
    ResponseCapability,
)


def test_contains_did():

    capability = ResponseCapability(
        citizen_did="did:tcn:test:01",
        response_capable=True,
    )

    assert capability.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_capability():

    capability = ResponseCapability(
        citizen_did="did:tcn:test:01",
        response_capable=True,
    )

    assert capability.response_capable is True


def test_serializes():

    capability = ResponseCapability(
        citizen_did="did:tcn:test:01",
        response_capable=True,
    )

    assert capability.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "response_capable": True,
    }
