from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionPolicy:

    policy_name: str
    requirements: list

    def to_dict(self):

        return {
            "policy_name":
                self.policy_name,
            "requirements":
                self.requirements,
        }
