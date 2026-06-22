from phase4.rights_permissions_layer.rights_verifier import (
    RightsVerifier,
)

from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)

from phase4.rights_permissions_layer.rights_bundle import (
    RightsBundle,
)


def test_all_permissions_granted():

    bundle = RightsBundle(
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

    assert (
        RightsVerifier.verify(bundle)
        is True
    )


def test_missing_permission():

    bundle = RightsBundle(
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
                granted=False,
            ),
        ],
    )

    assert (
        RightsVerifier.verify(bundle)
        is False
    )
