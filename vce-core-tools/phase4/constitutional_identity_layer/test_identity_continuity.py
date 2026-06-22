from phase4.constitutional_identity_layer.identity_continuity import (
    IdentityContinuity,
)


def test_contains_identity():

    continuity = IdentityContinuity(
        identity_id="identity-001",
        continuous=True,
    )

    assert continuity.identity_id == "identity-001"


def test_contains_continuity():

    continuity = IdentityContinuity(
        identity_id="identity-001",
        continuous=True,
    )

    assert continuity.continuous is True


def test_serializes():

    continuity = IdentityContinuity(
        identity_id="identity-001",
        continuous=True,
    )

    assert continuity.to_dict() == {
        "identity_id": "identity-001",
        "continuous": True,
    }
