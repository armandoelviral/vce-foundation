from phase4.rights_permissions_layer.rights_bundle import (
    RightsBundle,
)

from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)


def test_contains_did():

    bundle = build_bundle()

    assert bundle.citizen_did == "did:tcn:test:01"


def test_contains_permissions():

    bundle = build_bundle()

    assert len(bundle.permissions) == 2


def test_serializes():

    bundle = build_bundle()

    data = bundle.to_dict()

    assert data["citizen_did"] == "did:tcn:test:01"
    assert len(data["permissions"]) == 2


def build_bundle():

    return RightsBundle(
        citizen_did="did:tcn:test:01",
        permissions=[
            PermissionRecord(
                citizen_did="did:tcn:test:01",
                permission_name="submit_claim",
                granted=True,
            ),
            PermissionRecord(
                citizen_did="did:tcn:test:01",
                permission_name="vote_governance",
                granted=True,
            ),
        ],
    )
