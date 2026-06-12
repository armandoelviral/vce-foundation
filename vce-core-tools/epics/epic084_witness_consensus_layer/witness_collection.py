class WitnessCollection:

    def __init__(
        self,
        votes=None,
    ):

        self._votes = (
            votes
            if votes is not None
            else []
        )

    def add_vote(
        self,
        vote,
    ):

        self._votes.append(
            vote
        )

    def all_votes(
        self,
    ):

        return list(
            self._votes
        )

    def observed_votes(
        self,
    ):

        return [
            vote
            for vote in self._votes
            if vote.observed is True
        ]

    def total_count(
        self,
    ):

        return len(
            self._votes
        )

    def observed_count(
        self,
    ):

        return len(
            self.observed_votes()
        )
