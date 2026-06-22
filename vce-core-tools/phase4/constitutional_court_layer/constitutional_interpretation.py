from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalInterpretation:

    review_id: str
    interpretation: str

    def to_dict(self):

        return {
            "review_id":
                self.review_id,
            "interpretation":
                self.interpretation,
        }
