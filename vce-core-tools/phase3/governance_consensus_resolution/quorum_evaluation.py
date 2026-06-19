class QuorumEvaluation:

    MINIMUM_VOTES = 3

    @staticmethod
    def evaluate(
        vote_count: int,
    ) -> bool:

        return (
            vote_count
            >= QuorumEvaluation.MINIMUM_VOTES
        )
