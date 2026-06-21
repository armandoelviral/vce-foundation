from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SP1ProofRequest:

    request_id: str
    program_id: str
    input_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "request_id": self.request_id,
            "program_id": self.program_id,
            "input_hash": self.input_hash,
        }
