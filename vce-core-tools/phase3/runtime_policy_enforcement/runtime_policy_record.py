from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RuntimePolicyRecord:

    policy_id: str
    resource_type: str
    action: str
    effect: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "policy_id":
                self.policy_id,

            "resource_type":
                self.resource_type,

            "action":
                self.action,

            "effect":
                self.effect,
        }
