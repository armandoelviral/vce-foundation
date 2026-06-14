from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WASIImportReference:
    module: str
    name: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "module": self.module,
            "name": self.name,
        }
