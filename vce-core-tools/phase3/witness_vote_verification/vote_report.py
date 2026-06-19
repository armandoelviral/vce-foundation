class VoteReport:

    def __init__(
        self,
        votes,
    ):

        self.votes = votes

    def vote_count(
        self,
    ) -> int:

        return len(
            self.votes
        )

    def vote_ids(
        self,
    ):

        return list(
            self.votes.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "vote_count":
                self.vote_count(),

            "vote_ids":
                self.vote_ids(),
        }
