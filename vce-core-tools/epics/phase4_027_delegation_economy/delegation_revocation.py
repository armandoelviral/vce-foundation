from dataclasses import dataclass


@dataclass(frozen=True)
class DelegationRevocationRecord:
    revocation_id: str
    delegation_id: str
    reason: str

    def __post_init__(self):
        if not self.revocation_id:
            raise ValueError("revocation_id is required")

        if not self.delegation_id:
            raise ValueError("delegation_id is required")

        if not self.reason:
            raise ValueError("reason is required")
