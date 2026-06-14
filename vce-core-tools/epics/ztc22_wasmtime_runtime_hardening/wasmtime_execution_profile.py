from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Set
from typing import Union


@dataclass(frozen=True)
class WasmtimeExecutionProfile:
    max_fuel: int
    max_memory_bytes: int
    allowed_imports: Set[str]
    deterministic_required: bool

    def to_dict(self) -> Dict[str, Union[int, bool, List[str]]]:
        return {
            "max_fuel": self.max_fuel,
            "max_memory_bytes": self.max_memory_bytes,
            "allowed_imports": sorted(self.allowed_imports),
            "deterministic_required": self.deterministic_required,
        }
