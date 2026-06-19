from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PolicyVersionRecord:

    policy_id: str
    version: str
    approved_by: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "approved_by": self.approved_by,
        }
