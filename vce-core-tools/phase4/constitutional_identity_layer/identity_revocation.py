from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityRevocation:

    identity_id: str
    revoked: bool

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "revoked": self.revoked,
        }
