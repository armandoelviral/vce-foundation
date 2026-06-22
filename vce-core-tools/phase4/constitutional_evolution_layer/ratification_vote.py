from dataclasses import dataclass


@dataclass(frozen=True)
class RatificationVote:

    amendment_id: str
    approved: bool

    def to_dict(self):

        return {
            "amendment_id":
                self.amendment_id,
            "approved":
                self.approved,
        }
