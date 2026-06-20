from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProofResultRecord:

    result_id: str
    job_id: str
    proof_hash: str
    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "result_id": self.result_id,
            "job_id": self.job_id,
            "proof_hash": self.proof_hash,
            "status": self.status,
        }
