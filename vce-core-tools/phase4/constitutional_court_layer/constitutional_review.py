from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalReview:

    review_id: str
    challenge_id: str

    def to_dict(self):

        return {
            "review_id":
                self.review_id,
            "challenge_id":
                self.challenge_id,
        }
