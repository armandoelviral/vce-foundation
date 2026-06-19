from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)


class VoteRegistry:

    def __init__(self):

        self._votes = {}

    def add(
        self,
        vote: WitnessVoteRecord,
    ) -> None:

        self._votes[
            vote.vote_id
        ] = vote

    def get(
        self,
        vote_id: str,
    ):

        return self._votes.get(
            vote_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._votes
        )

    def vote_ids(
        self,
    ):

        return list(
            self._votes.keys()
        )
