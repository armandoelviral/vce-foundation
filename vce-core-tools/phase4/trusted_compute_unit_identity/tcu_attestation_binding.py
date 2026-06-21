from dataclasses import dataclass


@dataclass(frozen=True)
class TcuAttestationBinding:

    identity_hash: str
    attestation_root: str

    def to_dict(self):

        return {
            "identity_hash":
                self.identity_hash,
            "attestation_root":
                self.attestation_root,
        }
