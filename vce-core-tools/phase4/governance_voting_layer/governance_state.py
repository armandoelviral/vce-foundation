from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceState:

    governance_state: str

    def to_dict(self):

        return {
            "governance_state":
                self.governance_state,
        }
