from dataclasses import dataclass


@dataclass(frozen=True)
class IdentityRecovery:

    identity_id: str
    recovered: bool

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "recovered": self.recovered,
        }
