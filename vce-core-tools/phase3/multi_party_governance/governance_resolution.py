from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceResolution:

    status: str

    @staticmethod
    def from_quorum(
        quorum: bool,
    ):

        return GovernanceResolution(
            status=(
                "RESOLVED"
                if quorum
                else "UNRESOLVED"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
