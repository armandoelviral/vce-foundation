from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional


@dataclass(frozen=True)
class NativeExecutionResult:
    module_hash: str
    function_name: str
    output_payload: Dict[str, Any]
    success: bool
    trap: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module_hash": self.module_hash,
            "function_name": self.function_name,
            "output_payload": self.output_payload,
            "success": self.success,
            "trap": self.trap,
        }
