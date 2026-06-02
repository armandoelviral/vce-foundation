class StateSelector:

    def select(self, states):

        if not states:
            return None

        return max(
            states,
            key=lambda s:
            s["sequence_number"]
        )
