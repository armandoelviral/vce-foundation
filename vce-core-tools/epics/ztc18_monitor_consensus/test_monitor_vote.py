from epics.ztc18_monitor_consensus.monitor_vote import (
    MonitorVote,
)


def test_vote_contains_monitor_id():

    vote = MonitorVote(
        monitor_id="monitor-001",
        incident_id="incident-001",
        vote=True,
    )

    assert vote.monitor_id == "monitor-001"


def test_vote_contains_incident_id():

    vote = MonitorVote(
        monitor_id="monitor-001",
        incident_id="incident-001",
        vote=True,
    )

    assert vote.incident_id == "incident-001"


def test_vote_serializes():

    vote = MonitorVote(
        monitor_id="monitor-001",
        incident_id="incident-001",
        vote=True,
    )

    assert vote.to_dict() == {
        "monitor_id": "monitor-001",
        "incident_id": "incident-001",
        "vote": True,
    }
