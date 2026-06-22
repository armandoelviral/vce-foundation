from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalChallenge:

    challenge_id: str
    amendment_id: str

    def to_dict(self):

        return {
            "challenge_id":
                self.challenge_id,
            "amendment_id":
                self.amendment_id,
        }
