from dataclasses import dataclass


@dataclass(frozen=True)
class DutyAppeal:

    appeal_id: str
    violation_id: str

    def to_dict(self):

        return {
            "appeal_id": self.appeal_id,
            "violation_id": self.violation_id,
        }
