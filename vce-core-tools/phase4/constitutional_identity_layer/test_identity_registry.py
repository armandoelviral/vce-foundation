from phase4.constitutional_identity_layer.identity_registry import (
    IdentityRegistry,
)

from phase4.constitutional_identity_layer.identity_right import (
    IdentityRight,
)


def test_contains_identities():

    registry = IdentityRegistry(
        identities=[
            IdentityRight(
                identity_id="identity-001",
                right_name="identity_ownership",
            ),
        ]
    )

    assert len(registry.identities) == 1


def test_serializes():

    registry = IdentityRegistry(
        identities=[
            IdentityRight(
                identity_id="identity-001",
                right_name="identity_ownership",
            ),
        ]
    )

    assert registry.to_dict() == {
        "identities": [
            {
                "identity_id": "identity-001",
                "right_name": "identity_ownership",
            }
        ]
    }
