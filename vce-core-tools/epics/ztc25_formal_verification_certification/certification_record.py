from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class CertificationRecord:

    certification_id: str
    certified: bool
    reason: str

    def to_dict(self) -> Dict[str, Union[str, bool]]:

        return {
            "certification_id": self.certification_id,
            "certified": self.certified,
            "reason": self.reason,
        }
