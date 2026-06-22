from dataclasses import dataclass


@dataclass(frozen=True)
class RightsAppeal:

    appeal_id: str
    violation_id: str

    def to_dict(self):

        return {
            "appeal_id": self.appeal_id,
            "violation_id": self.violation_id,
        }
