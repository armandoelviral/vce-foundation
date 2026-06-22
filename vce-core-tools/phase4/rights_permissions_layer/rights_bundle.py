from dataclasses import dataclass
from typing import List

from phase4.rights_permissions_layer.permission_record import (
    PermissionRecord,
)


@dataclass(frozen=True)
class RightsBundle:

    citizen_did: str
    permissions: List[PermissionRecord]

    def to_dict(self):

        return {
            "citizen_did": self.citizen_did,
            "permissions": [
                permission.to_dict()
                for permission in self.permissions
            ],
        }
