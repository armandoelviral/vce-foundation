from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class PolicyRecord:

    policy_id: str
    version: int
    rule: str

    def to_dict(self) -> Dict[str, Union[str, int]]:

        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "rule": self.rule,
        }
