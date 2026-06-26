from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationRecord:
    delegation_id: str
    decision_id: str
    assignee: str

    def __post_init__(self):
        if not self.delegation_id:
            raise ValueError("delegation_id is required")

        if not self.decision_id:
            raise ValueError("decision_id is required")

        if not self.assignee:
            raise ValueError("assignee is required")
