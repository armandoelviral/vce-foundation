from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProofArtifactRecord:

    artifact_id: str
    execution_request_id: str
    prover_type: str
    proof_hash: str
    verification_status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "artifact_id":
                self.artifact_id,

            "execution_request_id":
                self.execution_request_id,

            "prover_type":
                self.prover_type,

            "proof_hash":
                self.proof_hash,

            "verification_status":
                self.verification_status,
        }
