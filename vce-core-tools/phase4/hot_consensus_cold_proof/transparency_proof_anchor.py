from dataclasses import dataclass
from typing import Dict

from phase4.hot_consensus_cold_proof.proof_attachment import (
    ProofAttachment,
)


@dataclass(frozen=True)
class TransparencyProofAnchor:

    anchor_id: str
    execution_request_id: str
    result_id: str
    proof_hash: str

    @staticmethod
    def anchor(
        anchor_id: str,
        attachment: ProofAttachment,
    ):

        return TransparencyProofAnchor(
            anchor_id=anchor_id,
            execution_request_id=attachment.execution_request_id,
            result_id=attachment.result_id,
            proof_hash=attachment.proof_hash,
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "anchor_id": self.anchor_id,
            "execution_request_id": self.execution_request_id,
            "result_id": self.result_id,
            "proof_hash": self.proof_hash,
        }
