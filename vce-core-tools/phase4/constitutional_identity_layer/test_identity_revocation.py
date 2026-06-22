from phase4.constitutional_identity_layer.identity_revocation import (
    IdentityRevocation,
)


def test_contains_identity():

    revocation = IdentityRevocation(
        identity_id="identity-001",
        revoked=True,
    )

    assert revocation.identity_id == "identity-001"


def test_contains_revoked():

    revocation = IdentityRevocation(
        identity_id="identity-001",
        revoked=True,
    )

    assert revocation.revoked is True


def test_serializes():

    revocation = IdentityRevocation(
        identity_id="identity-001",
        revoked=True,
    )

    assert revocation.to_dict() == {
        "identity_id": "identity-001",
        "revoked": True,
    }
