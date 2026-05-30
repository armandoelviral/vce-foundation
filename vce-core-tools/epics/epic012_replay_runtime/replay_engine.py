from replay_state import ReplayState


class ReplayEngine:

    def replay(
        self,
        event_stream
    ):

        state = ReplayState()

        for event in event_stream:

            state.append_event(
                event
            )

        return state
