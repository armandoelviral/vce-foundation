from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityContinuity:

    identity_id: str
    continuous: bool

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "continuous": self.continuous,
        }
