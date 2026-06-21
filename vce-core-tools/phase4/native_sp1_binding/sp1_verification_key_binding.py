from dataclasses import dataclass


@dataclass(frozen=True)
class SP1VerificationKeyBinding:

    tcu_did: str
    verification_key: str

    def to_dict(self):

        return {
            "tcu_did": self.tcu_did,
            "verification_key":
                self.verification_key,
        }
