from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProofObligation:

    obligation_id: str
    invariant_id: str
    description: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "obligation_id": self.obligation_id,
            "invariant_id": self.invariant_id,
            "description": self.description,
        }
