class PropertyBasedReplayTesting:

    @staticmethod
    def validate(
        state: dict,
    ) -> bool:

        if (
            state["current_sequence"]
            < state["previous_sequence"]
        ):
            return False

        if state["event_count"] < 0:
            return False

        if not state["state_hash"]:
            return False

        return True
