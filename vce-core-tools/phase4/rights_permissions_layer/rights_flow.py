from phase4.rights_permissions_layer.permission_grant import (
    PermissionGrant,
)

from phase4.rights_permissions_layer.rights_bundle import (
    RightsBundle,
)

from phase4.rights_permissions_layer.rights_state import (
    RightsState,
)

from phase4.rights_permissions_layer.rights_verifier import (
    RightsVerifier,
)


class RightsFlow:

    @staticmethod
    def generate():

        permissions = [
            PermissionGrant.grant(
                citizen_did="did:tcn:test:01",
                permission_name="submit_claim",
            ),
            PermissionGrant.grant(
                citizen_did="did:tcn:test:01",
                permission_name="vote_governance",
            ),
        ]

        bundle = RightsBundle(
            citizen_did="did:tcn:test:01",
            permissions=permissions,
        )

        state = RightsState(
            citizen_did="did:tcn:test:01",
            rights_state="ACTIVE",
        )

        authorized = RightsVerifier.verify(
            bundle
        )

        return {
            "permissions": [
                permission.to_dict()
                for permission in permissions
            ],
            "state": state.to_dict(),
            "authorized": authorized,
        }
