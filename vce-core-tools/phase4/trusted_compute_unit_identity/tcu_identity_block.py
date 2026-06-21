from dataclasses import dataclass


@dataclass(frozen=True)
class TcuIdentityBlock:

    did: str
    ed25519_public_key: str
    mldsa65_public_key: str

    def to_dict(self):

        return {
            "did": self.did,
            "ed25519_public_key":
                self.ed25519_public_key,
            "mldsa65_public_key":
                self.mldsa65_public_key,
        }
