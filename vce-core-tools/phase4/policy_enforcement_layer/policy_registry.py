from dataclasses import dataclass
from typing import List

from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


@dataclass(frozen=True)
class PolicyRegistry:

    policies: List[PolicyRecord]

    def to_dict(self):

        return {
            "policies": [
                policy.to_dict()
                for policy in self.policies
            ]
        }
