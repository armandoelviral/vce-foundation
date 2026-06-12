from dataclasses import dataclass


@dataclass(frozen=True)
class ConsensusPolicy:
    policy_id: str
    required_votes: int
    total_witnesses: int

    def is_satisfied(
        self,
        observed_votes: int,
    ):

        return observed_votes >= self.required_votes

    def policy_label(self):

        return (
            f"{self.required_votes}-of-{self.total_witnesses}"
        )
