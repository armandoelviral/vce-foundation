from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WasmtimeExecutionAttestation:
    module_hash: str
    function_name: str
    execution_hash: str
    verified: bool

    def to_dict(self) -> Dict:
        return {
            "module_hash": self.module_hash,
            "function_name": self.function_name,
            "execution_hash": self.execution_hash,
            "verified": self.verified,
        }
