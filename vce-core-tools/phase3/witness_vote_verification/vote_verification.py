from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)


class VoteVerification:

    ALLOWED_VALUES = {
        "APPROVE",
        "REJECT",
        "ABSTAIN",
    }

    @staticmethod
    def verify(
        vote: WitnessVoteRecord,
    ) -> bool:

        if not vote.vote_id:
            return False

        if not vote.witness_did:
            return False

        if (
            vote.vote_value
            not in VoteVerification.ALLOWED_VALUES
        ):
            return False

        return True
