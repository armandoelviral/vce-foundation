from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalDecision:

    review_id: str
    decision: str

    def to_dict(self):

        return {
            "review_id":
                self.review_id,
            "decision":
                self.decision,
        }
