from dataclasses import dataclass
from typing import Dict

from phase4.hot_consensus_cold_proof.proof_result_record import (
    ProofResultRecord,
)


@dataclass(frozen=True)
class ProofAttachment:

    execution_request_id: str
    result_id: str
    proof_hash: str

    @staticmethod
    def attach(
        execution_request_id: str,
        proof_result: ProofResultRecord,
    ):

        return ProofAttachment(
            execution_request_id=execution_request_id,
            result_id=proof_result.result_id,
            proof_hash=proof_result.proof_hash,
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "execution_request_id":
                self.execution_request_id,

            "result_id":
                self.result_id,

            "proof_hash":
                self.proof_hash,
        }
