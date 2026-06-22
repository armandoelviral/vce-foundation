from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationEvent:

    citizen_did: str
    event_type: str
    impact: int

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "event_type":
                self.event_type,
            "impact":
                self.impact,
        }
