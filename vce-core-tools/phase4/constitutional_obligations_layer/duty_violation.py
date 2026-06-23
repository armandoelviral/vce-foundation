from dataclasses import dataclass


@dataclass(frozen=True)
class DutyViolation:

    duty_id: str
    violation_type: str

    def to_dict(self):

        return {
            "duty_id": self.duty_id,
            "violation_type": self.violation_type,
        }
