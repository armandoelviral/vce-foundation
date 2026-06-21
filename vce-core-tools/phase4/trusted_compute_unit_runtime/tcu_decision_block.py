from dataclasses import dataclass
from typing import Dict, Union


@dataclass(frozen=True)
class TcuDecisionBlock:

    verdict: str
    execution_status: str
    compute_gas_used: int
    system_state_root: str

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "verdict": self.verdict,
            "execution_status": self.execution_status,
            "compute_gas_used": self.compute_gas_used,
            "system_state_root": self.system_state_root,
        }
