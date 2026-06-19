from phase3.governance_consensus_resolution.quorum_evaluation import (
    QuorumEvaluation,
)


def test_quorum_reached():

    assert (
        QuorumEvaluation.evaluate(
            vote_count=3
        )
        is True
    )


def test_quorum_above_threshold():

    assert (
        QuorumEvaluation.evaluate(
            vote_count=5
        )
        is True
    )


def test_quorum_not_reached():

    assert (
        QuorumEvaluation.evaluate(
            vote_count=2
        )
        is False
    )


def test_zero_votes_fails():

    assert (
        QuorumEvaluation.evaluate(
            vote_count=0
        )
        is False
    )
