from epics.ztc18_monitor_consensus.monitor_vote import (
    MonitorVote,
)

from epics.ztc18_monitor_consensus.monitor_vote_registry import (
    MonitorVoteRegistry,
)


def test_registry_stores_vote():

    registry = MonitorVoteRegistry()

    vote = MonitorVote(
        monitor_id="monitor-001",
        incident_id="incident-001",
        vote=True,
    )

    registry.add(vote)

    assert registry.count() == 1


def test_registry_returns_votes():

    registry = MonitorVoteRegistry()

    vote = MonitorVote(
        monitor_id="monitor-001",
        incident_id="incident-001",
        vote=True,
    )

    registry.add(vote)

    votes = registry.all()

    assert len(votes) == 1
    assert votes[0].monitor_id == "monitor-001"


def test_registry_starts_empty():

    registry = MonitorVoteRegistry()

    assert registry.count() == 0
