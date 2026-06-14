from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DisasterRecoveryPlan:

    plan_id: str
    recovery_target: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "plan_id": self.plan_id,
            "recovery_target": self.recovery_target,
        }
