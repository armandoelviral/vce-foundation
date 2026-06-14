from dataclasses import dataclass
from typing import Any
from typing import Dict


@dataclass(frozen=True)
class WasmtimeExecutionRequest:
    module_hash: str
    function_name: str
    input_payload: Dict[str, Any]


@dataclass(frozen=True)
class WasmtimeExecutionResult:
    module_hash: str
    function_name: str
    output_payload: Dict[str, Any]
    success: bool
