from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityRight:

    identity_id: str
    right_name: str

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "right_name": self.right_name,
        }
