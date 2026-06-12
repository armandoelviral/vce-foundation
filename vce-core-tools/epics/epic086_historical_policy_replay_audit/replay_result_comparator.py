class ReplayResultComparator:

    def compare(
        self,
        original_decision,
        replay_decision,
    ):

        if original_decision == replay_decision:
            return {
                "result": "REPLAY_MATCH",
                "original_decision": original_decision,
                "replay_decision": replay_decision,
            }

        return {
            "result": "REPLAY_MISMATCH",
            "original_decision": original_decision,
            "replay_decision": replay_decision,
        }
