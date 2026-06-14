class MonitorConsensusPolicy:

    def has_consensus(
        self,
        total_monitors: int,
        affirmative_votes: int,
    ) -> bool:

        required_votes = (
            total_monitors // 2
        ) + 1

        return (
            affirmative_votes
            >= required_votes
        )
