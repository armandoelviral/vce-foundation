from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationRecord:
    delegation_id: str
    delegator_id: str
    delegate_id: str
    delegated_capacity: int
    reason: str

    def __post_init__(self):
        if not self.delegation_id:
            raise ValueError("delegation_id is required")

        if not self.delegator_id:
            raise ValueError("delegator_id is required")

        if not self.delegate_id:
            raise ValueError("delegate_id is required")

        if self.delegated_capacity <= 0:
            raise ValueError("delegated_capacity must be positive")

        if not self.reason:
            raise ValueError("reason is required")
