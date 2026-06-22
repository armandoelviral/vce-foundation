from phase4.constitutional_identity_layer.identity_right import (
    IdentityRight,
)


def test_contains_identity_id():

    right = IdentityRight(
        identity_id="identity-001",
        right_name="identity_ownership",
    )

    assert right.identity_id == "identity-001"


def test_contains_right_name():

    right = IdentityRight(
        identity_id="identity-001",
        right_name="identity_ownership",
    )

    assert (
        right.right_name
        == "identity_ownership"
    )


def test_serializes():

    right = IdentityRight(
        identity_id="identity-001",
        right_name="identity_ownership",
    )

    assert right.to_dict() == {
        "identity_id": "identity-001",
        "right_name": "identity_ownership",
    }

