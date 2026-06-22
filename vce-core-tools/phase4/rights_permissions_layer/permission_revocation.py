from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)


class PermissionRevocation:

    @staticmethod
    def revoke(
        citizen_did: str,
        permission_name: str,
    ) -> PermissionRecord:

        return PermissionRecord(
            citizen_did=citizen_did,
            permission_name=permission_name,
            granted=False,
        )
