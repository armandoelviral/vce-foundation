class MajorityDecision:

    @staticmethod
    def decide(
        approve_votes: int,
        reject_votes: int,
    ) -> str:

        if approve_votes > reject_votes:
            return "APPROVED"

        return "REJECTED"
