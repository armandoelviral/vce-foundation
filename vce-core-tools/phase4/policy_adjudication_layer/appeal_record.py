from dataclasses import dataclass


@dataclass(frozen=True)
class AppealRecord:

    appeal_id: str
    decision_id: str
    status: str

    def to_dict(self):

        return {
            "appeal_id":
                self.appeal_id,
            "decision_id":
                self.decision_id,
            "status":
                self.status,
        }
