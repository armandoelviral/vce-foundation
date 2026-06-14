from epics.ztc18_monitor_consensus.monitor_consensus_policy import (
    MonitorConsensusPolicy,
)


def test_two_of_three_reaches_consensus():

    policy = MonitorConsensusPolicy()

    assert policy.has_consensus(
        total_monitors=3,
        affirmative_votes=2,
    )


def test_one_of_three_does_not_reach_consensus():

    policy = MonitorConsensusPolicy()

    assert not policy.has_consensus(
        total_monitors=3,
        affirmative_votes=1,
    )


def test_three_of_five_reaches_consensus():

    policy = MonitorConsensusPolicy()

    assert policy.has_consensus(
        total_monitors=5,
        affirmative_votes=3,
    )
