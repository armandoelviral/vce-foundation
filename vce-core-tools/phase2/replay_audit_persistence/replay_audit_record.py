from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class ReplayAuditRecord:

    replay_id: str
    audit_result: bool

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool]]:

        return {
            "replay_id": self.replay_id,
            "audit_result": self.audit_result,
        }
