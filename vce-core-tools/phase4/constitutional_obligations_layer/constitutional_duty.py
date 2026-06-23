from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalDuty:

    duty_id: str
    duty_name: str

    def to_dict(self):

        return {
            "duty_id": self.duty_id,
            "duty_name": self.duty_name,
        }
