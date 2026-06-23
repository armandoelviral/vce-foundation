from dataclasses import dataclass


@dataclass(frozen=True)
class DutyState:

    duty_state: str

    def to_dict(self):

        return {
            "duty_state": self.duty_state,
        }
