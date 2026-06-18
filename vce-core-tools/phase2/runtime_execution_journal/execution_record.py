from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExecutionRecord:

    execution_id: str
    opcode: str
    input_data: str
    output_data: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "execution_id": self.execution_id,
            "opcode": self.opcode,
            "input_data": self.input_data,
            "output_data": self.output_data,
        }
