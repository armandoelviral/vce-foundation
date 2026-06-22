from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceRequirement:

    required_state: str = "ACTIVE"

    def is_satisfied(
        self,
        governance_state: str,
    ) -> bool:

        return (
            governance_state
            == self.required_state
        )

    def to_dict(self):

        return {
            "requirement_type":
                "GOVERNANCE",
            "required_state":
                self.required_state,
        }
