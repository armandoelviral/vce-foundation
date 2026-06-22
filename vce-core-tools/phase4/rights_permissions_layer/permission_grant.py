from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)


class PermissionGrant:

    @staticmethod
    def grant(
        citizen_did: str,
        permission_name: str,
    ) -> PermissionRecord:

        return PermissionRecord(
            citizen_did=citizen_did,
            permission_name=permission_name,
            granted=True,
        )
