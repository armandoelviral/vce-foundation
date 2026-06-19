from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)


class GovernanceQuorumEvaluation:

    @staticmethod
    def evaluate(
        votes: list[GovernanceVoteRecord],
    ) -> bool:

        if not votes:
            return False

        approvals = sum(
            1
            for vote in votes
            if vote.vote == "APPROVE"
        )

        return (
            approvals
            > len(votes) / 2
        )
