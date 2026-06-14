from epics.ztc19_governance_ledger.governance_event import (
    GovernanceEvent,
)


class GovernanceAdmissionPolicy:

    ALLOWED_EVENT_TYPES = {
        "incident_declaration",
        "incident_escalation",
        "response_decision",
        "witness_suspension",
        "witness_recovery",
        "key_rotation",
        "monitor_consensus",
    }

    def accept(
        self,
        event: GovernanceEvent,
    ) -> bool:

        return (
            event.event_type
            in self.ALLOWED_EVENT_TYPES
        )
