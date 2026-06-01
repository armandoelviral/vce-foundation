class QuorumValidator:

    def __init__(
        self,
        threshold=2/3
    ):

        self.threshold = threshold


    def validate(
        self,
        votes
    ):

        total = len(
            votes
        )


        if total == 0:
            return {
                "consensus": False,
                "reason": "NO_VOTES"
            }


        approvals = sum(
            1
            for vote in votes
            if vote[
                "payload"
            ][
                "decision"
            ]
            ==
            "APPROVE"
        )


        ratio = (
            approvals
            /
            total
        )


        return {
            "consensus":
                ratio >= self.threshold,

            "approval_ratio":
                ratio,

            "votes":
                total
        }
