from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationState:

    citizen_did: str
    reputation_state: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "reputation_state":
                self.reputation_state,
        }
