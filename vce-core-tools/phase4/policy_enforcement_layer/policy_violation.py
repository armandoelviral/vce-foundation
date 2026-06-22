from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyViolation:

    policy_id: str
    violation_type: str

    def to_dict(self):

        return {
            "policy_id":
                self.policy_id,
            "violation_type":
                self.violation_type,
        }
