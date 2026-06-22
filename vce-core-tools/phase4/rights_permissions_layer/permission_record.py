from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionRecord:

    citizen_did: str
    permission_name: str
    granted: bool

    def to_dict(self):

        return {
            "citizen_did": self.citizen_did,
            "permission_name": self.permission_name,
            "granted": self.granted,
        }
