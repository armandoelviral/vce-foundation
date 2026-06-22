from dataclasses import dataclass


@dataclass(frozen=True)
class EligibilityEvaluation:

    citizen_did: str
    eligible: bool

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "eligible":
                self.eligible,
        }
