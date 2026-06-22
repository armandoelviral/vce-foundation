class ConsensusDecision:

    @staticmethod
    def decide(
        tally,
    ):

        decision = (
            "APPROVED"
            if tally["yes_votes"]
            > tally["no_votes"]
            else "REJECTED"
        )

        return {
            "proposal_id":
                tally["proposal_id"],
            "decision":
                decision,
        }
