class ConsensusFaultInjection:

    def inject(
        self,
        votes,
        fault_type=None,
    ):

        votes = list(votes)

        if fault_type is None:
            return votes

        if fault_type == "offline":

            return votes[:-1]

        if fault_type == "invalid_vote":

            if votes:
                votes[0] = (
                    not votes[0]
                )

            return votes

        return votes
