from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class AttestationAdmissionRecord:
    witness_id: str
    admitted: bool
    reason: str

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        return {
            "witness_id": self.witness_id,
            "admitted": self.admitted,
            "reason": self.reason,
        }
