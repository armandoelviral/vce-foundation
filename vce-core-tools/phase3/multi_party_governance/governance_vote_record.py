from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceVoteRecord:

    vote_id: str
    voter_id: str
    vote: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "vote_id": self.vote_id,
            "voter_id": self.voter_id,
            "vote": self.vote,
        }
