from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class PolicyReplayBinding:

    policy_id: str
    version: int
    replay_lsn: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "replay_lsn": self.replay_lsn,
        }
