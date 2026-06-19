from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TrustPolicyRecord:

    policy_id: str
    policy_name: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
        }
