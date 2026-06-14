from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class HardwareAdmissionRecord:
    provider: str
    admitted: bool
    reason: str

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        return {
            "provider": self.provider,
            "admitted": self.admitted,
            "reason": self.reason,
        }
