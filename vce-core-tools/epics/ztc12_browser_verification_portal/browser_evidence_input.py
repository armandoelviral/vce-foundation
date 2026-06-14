from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class BrowserEvidenceInput:
    raw_json: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "raw_json": self.raw_json,
        }
