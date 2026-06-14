from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class DeploymentApprovalRecord:

    release_id: str
    approved: bool
    reason: str

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool]]:

        return {
            "release_id": self.release_id,
            "approved": self.approved,
            "reason": self.reason,
        }
