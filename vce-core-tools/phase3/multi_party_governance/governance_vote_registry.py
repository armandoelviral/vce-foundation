from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)


class GovernanceVoteRegistry:

    def __init__(self):

        self._votes = {}

    def add(
        self,
        vote: GovernanceVoteRecord,
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
