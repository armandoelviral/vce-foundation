from dataclasses import dataclass

from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)

from phase4.trusted_compute_unit_identity.tcu_identity_signatures import (
    TcuIdentitySignatures,
)


@dataclass(frozen=True)
class TcuIdentityRecord:

    identity: TcuIdentityBlock
    identity_hash: str
    signatures: TcuIdentitySignatures

    def to_dict(self):

        return {
            "identity": self.identity.to_dict(),
            "identity_hash": self.identity_hash,
            "signatures": self.signatures.to_dict(),
        }
