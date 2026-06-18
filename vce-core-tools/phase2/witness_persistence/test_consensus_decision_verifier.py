from phase2.witness_persistence.consensus_decision_record import (
    ConsensusDecisionRecord,
)

from phase2.witness_persistence.consensus_decision_verifier import (
    ConsensusDecisionVerifier,
)


def test_verifier_accepts_sufficient_votes():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=3,
    )

    assert (
        ConsensusDecisionVerifier.verify(
            decision,
            required_votes=2,
        )
        is True
    )


def test_verifier_rejects_insufficient_votes():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=1,
    )

    assert (
        ConsensusDecisionVerifier.verify(
            decision,
            required_votes=2,
        )
        is False
    )


def test_verifier_rejects_unapproved_decision():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=False,
        vote_count=3,
    )

    assert (
        ConsensusDecisionVerifier.verify(
            decision,
            required_votes=2,
        )
        is False
    )
