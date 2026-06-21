from dataclasses import dataclass


@dataclass
class TcuRegistryEntry:

    did: str
    identity_hash: str
    attestation_root: str
    status: str

    def to_dict(self):

        return {
            "did": self.did,
            "identity_hash":
                self.identity_hash,
            "attestation_root":
                self.attestation_root,
            "status":
                self.status,
        }
