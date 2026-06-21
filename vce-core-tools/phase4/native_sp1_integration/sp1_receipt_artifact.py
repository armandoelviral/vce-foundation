from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SP1ReceiptArtifact:

    receipt_id: str
    request_id: str
    proof_hash: str
    verification_key_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "receipt_id":
                self.receipt_id,

            "request_id":
                self.request_id,

            "proof_hash":
                self.proof_hash,

            "verification_key_hash":
                self.verification_key_hash,
        }
