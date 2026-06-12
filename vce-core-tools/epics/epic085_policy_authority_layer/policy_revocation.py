from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyRevocation:
    policy_id: str
    policy_version: str
    revoked_by: str
    revoked_at: str
    reason: str
    active: bool = True

    def is_revoked(self):

        return self.active is True

    def to_dict(self):

        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "revoked_by": self.revoked_by,
            "revoked_at": self.revoked_at,
            "reason": self.reason,
            "active": self.active,
        }
