from dataclasses import dataclass


@dataclass(frozen=True)
class TcuIdentitySignatures:

    ed25519_signature: str
    mldsa65_signature: str

    def to_dict(self):

        return {
            "ed25519_signature":
                self.ed25519_signature,
            "mldsa65_signature":
                self.mldsa65_signature,
        }
