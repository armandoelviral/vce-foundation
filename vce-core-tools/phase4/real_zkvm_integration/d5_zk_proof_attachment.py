from dataclasses import dataclass
from typing import Dict

from phase4.real_zkvm_integration.proof_artifact_record import (
    ProofArtifactRecord,
)


@dataclass(frozen=True)
class D5zkProofAttachment:

    d5_artifact_id: str
    proof_artifact_id: str
    proof_hash: str

    @staticmethod
    def attach(
        d5_artifact_id: str,
        proof_artifact: ProofArtifactRecord,
    ):

        return D5zkProofAttachment(
            d5_artifact_id=d5_artifact_id,
            proof_artifact_id=proof_artifact.artifact_id,
            proof_hash=proof_artifact.proof_hash,
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "d5_artifact_id": self.d5_artifact_id,
            "proof_artifact_id": self.proof_artifact_id,
            "proof_hash": self.proof_hash,
        }
