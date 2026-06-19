from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessVoteRecord:

    vote_id: str
    witness_did: str
    vote_value: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "vote_id":
                self.vote_id,

            "witness_did":
                self.witness_did,

            "vote_value":
                self.vote_value,
        }
