from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)

from phase3.multi_party_governance.governance_quorum_evaluation import (
    GovernanceQuorumEvaluation,
)


def test_majority_approve_reaches_quorum():

    votes = [
        GovernanceVoteRecord(
            vote_id="1",
            voter_id="w1",
            vote="APPROVE",
        ),
        GovernanceVoteRecord(
            vote_id="2",
            voter_id="w2",
            vote="APPROVE",
        ),
        GovernanceVoteRecord(
            vote_id="3",
            voter_id="w3",
            vote="REJECT",
        ),
    ]

    result = (
        GovernanceQuorumEvaluation.evaluate(
            votes
        )
    )

    assert result is True


def test_majority_reject_fails_quorum():

    votes = [
        GovernanceVoteRecord(
            vote_id="1",
            voter_id="w1",
            vote="REJECT",
        ),
        GovernanceVoteRecord(
            vote_id="2",
            voter_id="w2",
            vote="REJECT",
        ),
        GovernanceVoteRecord(
            vote_id="3",
            voter_id="w3",
            vote="APPROVE",
        ),
    ]

    result = (
        GovernanceQuorumEvaluation.evaluate(
            votes
        )
    )

    assert result is False


def test_empty_vote_set_fails():

    result = (
        GovernanceQuorumEvaluation.evaluate(
            []
        )
    )

    assert result is False
