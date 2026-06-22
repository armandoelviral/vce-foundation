class VoteTally:

    @staticmethod
    def calculate(
        proposal_id,
        votes,
    ):

        yes_votes = sum(
            1
            for vote in votes
            if vote.vote == "YES"
        )

        no_votes = sum(
            1
            for vote in votes
            if vote.vote == "NO"
        )

        return {
            "proposal_id": proposal_id,
            "yes_votes": yes_votes,
            "no_votes": no_votes,
        }
