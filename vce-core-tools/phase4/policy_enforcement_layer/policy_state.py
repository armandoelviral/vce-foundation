from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyState:

    policy_id: str
    policy_state: str

    def to_dict(self):

        return {
            "policy_id":
                self.policy_id,
            "policy_state":
                self.policy_state,
        }
