from phase4.rights_permissions_layer.permission_grant import (
    PermissionGrant,
)


def test_creates_granted_permission():

    permission = PermissionGrant.grant(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert permission.granted is True


def test_contains_permission_name():

    permission = PermissionGrant.grant(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert (
        permission.permission_name
        == "submit_claim"
    )


def test_contains_did():

    permission = PermissionGrant.grant(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
    )

    assert (
        permission.citizen_did
        == "did:tcn:test:01"
    )
