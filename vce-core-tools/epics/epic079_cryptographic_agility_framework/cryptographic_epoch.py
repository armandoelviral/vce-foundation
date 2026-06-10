from dataclasses import dataclass


@dataclass(frozen=True)
class CryptographicEpoch:
    epoch_id: str
    signature_algorithm: str
    hash_algorithm: str
    active: bool
    introduced_at: str

    def to_dict(self):

        return {
            "epoch_id": self.epoch_id,
            "signature_algorithm": self.signature_algorithm,
            "hash_algorithm": self.hash_algorithm,
            "active": self.active,
            "introduced_at": self.introduced_at,
        }
