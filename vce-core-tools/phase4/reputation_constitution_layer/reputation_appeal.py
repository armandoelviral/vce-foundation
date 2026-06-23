from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationAppeal:

    appeal_id: str
    reputation_event: str

    def to_dict(self):

        return {
            "appeal_id": self.appeal_id,
            "reputation_event": self.reputation_event,
        }
