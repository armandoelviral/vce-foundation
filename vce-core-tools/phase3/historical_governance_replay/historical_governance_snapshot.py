from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HistoricalGovernanceSnapshot:

    snapshot_id: str
    policy_version: str
    authority_id: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "snapshot_id":
                self.snapshot_id,
            "policy_version":
                self.policy_version,
            "authority_id":
                self.authority_id,
        }
