from phase2.witness_persistence.consensus_decision_record import (
    ConsensusDecisionRecord,
)


class ConsensusDecisionVerifier:

    @staticmethod
    def verify(
        decision: ConsensusDecisionRecord,
        required_votes: int,
    ) -> bool:

        if not decision.approved:
            return False

        return (
            decision.vote_count
            >= required_votes
        )
