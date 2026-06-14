class QuorumMutationPolicy:

    def required_votes(
        self,
        total_witnesses: int,
        suspended_witnesses: int,
    ) -> int:

        active_witnesses = (
            total_witnesses
            - suspended_witnesses
        )

        if active_witnesses >= 2:
            return 2

        return 0
