from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class FormalInvariant:

    invariant_id: str
    description: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "invariant_id": self.invariant_id,
            "description": self.description,
        }
