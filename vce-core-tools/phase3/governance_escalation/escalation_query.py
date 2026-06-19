from phase3.governance_escalation.escalation_registry import (
    EscalationRegistry,
)


class EscalationQuery:

    def __init__(
        self,
        registry: EscalationRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        escalation_id: str,
    ):

        return self.registry.get(
            escalation_id
        )
