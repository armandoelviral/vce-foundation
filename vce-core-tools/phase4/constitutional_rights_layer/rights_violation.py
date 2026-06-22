from dataclasses import dataclass


@dataclass(frozen=True)
class RightsViolation:

    right_id: str
    violation_type: str

    def to_dict(self):

        return {
            "right_id": self.right_id,
            "violation_type": self.violation_type,
        }
