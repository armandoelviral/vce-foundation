from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WasmtimeModuleReference:
    module_hash: str
    module_name: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "module_hash": self.module_hash,
            "module_name": self.module_name,
        }
