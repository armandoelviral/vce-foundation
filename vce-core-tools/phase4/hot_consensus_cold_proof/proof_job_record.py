from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProofJobRecord:

    job_id: str
    execution_request_id: str
    prover_type: str
    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "job_id":
                self.job_id,

            "execution_request_id":
                self.execution_request_id,

            "prover_type":
                self.prover_type,

            "status":
                self.status,
        }
