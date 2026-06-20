from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PolicyActivationRecord:

    activation_id: str
    policy_id: str
    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "activation_id": self.activation_id,
            "policy_id": self.policy_id,
            "status": self.status,
        }
