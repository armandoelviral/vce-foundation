from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.state_transition_applier import (
    StateTransitionApplier,
)


class IncrementalReplayFromSnapshot:

    def __init__(
        self,
    ):

        self.applier = StateTransitionApplier()

    def rebuild(
        self,
        snapshot_state: RuntimeState,
        events,
    ) -> RuntimeState:

        state = snapshot_state

        for event in events:

            state = self.applier.apply(
                state=state,
                event=event,
            )

        return state
