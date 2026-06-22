from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)


def test_contains_did():

    permission = PermissionRecord(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
        granted=True,
    )

    assert permission.citizen_did == "did:tcn:test:01"


def test_contains_permission_name():

    permission = PermissionRecord(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
        granted=True,
    )

    assert permission.permission_name == "submit_claim"


def test_contains_granted():

    permission = PermissionRecord(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
        granted=True,
    )

    assert permission.granted is True


def test_serializes():

    permission = PermissionRecord(
        citizen_did="did:tcn:test:01",
        permission_name="submit_claim",
        granted=True,
    )

    assert permission.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "permission_name": "submit_claim",
        "granted": True,
    }

