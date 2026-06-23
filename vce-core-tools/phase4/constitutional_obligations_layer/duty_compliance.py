from dataclasses import dataclass


@dataclass(frozen=True)
class DutyCompliance:

    duty_id: str
    compliant: bool

    def to_dict(self):

        return {
            "duty_id": self.duty_id,
            "compliant": self.compliant,
        }
