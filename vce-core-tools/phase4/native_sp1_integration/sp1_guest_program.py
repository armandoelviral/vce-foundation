from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SP1GuestProgram:

    program_id: str
    input_hash: str
    output_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "program_id": self.program_id,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
        }
