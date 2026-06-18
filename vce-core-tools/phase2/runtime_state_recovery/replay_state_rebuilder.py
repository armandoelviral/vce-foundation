from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.state_transition_applier import (
    StateTransitionApplier,
)


class ReplayStateRebuilder:

    def __init__(
        self,
    ):

        self.applier = StateTransitionApplier()

    def rebuild(
        self,
        events,
    ) -> RuntimeState:

        state = RuntimeState()

        for event in events:

            state = self.applier.apply(
                state=state,
                event=event,
            )

        return state
