from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyApproval:
    policy_id: str
    policy_version: str
    approved_by: str
    approved_at: str
    approval_status: str

    def is_approved(self):

        return self.approval_status == "APPROVED"

    def to_dict(self):

        return {
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "approval_status": self.approval_status,
        }
