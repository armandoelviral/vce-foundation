from phase4.rights_permissions_layer.permission_revocation import (
    PermissionRevocation,
)


def test_creates_revoked_permission():

    permission = PermissionRevocation.revoke(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert permission.granted is False


def test_contains_permission_name():

    permission = PermissionRevocation.revoke(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert (
        permission.permission_name
        == "submit_claim"
    )


def test_contains_did():

    permission = PermissionRevocation.revoke(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert (
        permission.citizen_did
        == "did:tcn:test:01"
    )
