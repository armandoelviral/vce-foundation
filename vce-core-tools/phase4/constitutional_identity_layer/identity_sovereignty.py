from dataclasses import dataclass


@dataclass(frozen=True)
class IdentitySovereignty:

    identity_id: str
    sovereign: bool

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "sovereign": self.sovereign,
        }
