from dataclasses import dataclass
from typing import Dict

from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)


@dataclass(frozen=True)
class D5RealProofAttachment:

    d5_artifact_id: str
    receipt_id: str
    proof_hash: str
    verification_key_hash: str

    @staticmethod
    def attach(
        d5_artifact_id: str,
        receipt: SP1ReceiptArtifact,
    ):

        return D5RealProofAttachment(
            d5_artifact_id=d5_artifact_id,
            receipt_id=receipt.receipt_id,
            proof_hash=receipt.proof_hash,
            verification_key_hash=(
                receipt.verification_key_hash
            ),
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "d5_artifact_id":
                self.d5_artifact_id,

            "receipt_id":
                self.receipt_id,

            "proof_hash":
                self.proof_hash,

            "verification_key_hash":
                self.verification_key_hash,
        }
