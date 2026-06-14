from epics.ztc18_monitor_consensus.monitor_vote import (
    MonitorVote,
)

from epics.ztc18_monitor_consensus.monitor_vote_registry import (
    MonitorVoteRegistry,
)

from epics.ztc18_monitor_consensus.monitor_consensus_policy import (
    MonitorConsensusPolicy,
)

from epics.ztc18_monitor_consensus.incident_declaration import (
    IncidentDeclaration,
)

from epics.ztc18_monitor_consensus.incident_registry import (
    IncidentRegistry,
)

from epics.ztc18_monitor_consensus.incident_escalation_record import (
    IncidentEscalationRecord,
)

from epics.ztc18_monitor_consensus.incident_response_decision import (
    IncidentResponseDecision,
)


def test_end_to_end_monitor_consensus_flow():

    vote_registry = MonitorVoteRegistry()

    vote_registry.add(
        MonitorVote(
            monitor_id="monitor-001",
            incident_id="incident-001",
            vote=True,
        )
    )

    vote_registry.add(
        MonitorVote(
            monitor_id="monitor-002",
            incident_id="incident-001",
            vote=True,
        )
    )

    vote_registry.add(
        MonitorVote(
            monitor_id="monitor-003",
            incident_id="incident-001",
            vote=False,
        )
    )

    policy = MonitorConsensusPolicy()

    consensus = policy.has_consensus(
        total_monitors=3,
        affirmative_votes=2,
    )

    assert consensus is True

    declaration = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=consensus,
    )

    registry = IncidentRegistry()

    registry.add(
        declaration
    )

    assert registry.count() == 1

    escalation = IncidentEscalationRecord(
        incident_id="incident-001",
        action="suspend_witness",
        target="witness-003",
    )

    decision = IncidentResponseDecision(
        incident_id="incident-001",
        approved=True,
    )

    assert declaration.declared is True
    assert escalation.action == "suspend_witness"
    assert decision.approved is True
