from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyRecord:

    policy_id: str
    policy_name: str
    active: bool

    def to_dict(self):

        return {
            "policy_id":
                self.policy_id,
            "policy_name":
                self.policy_name,
            "active":
                self.active,
        }
