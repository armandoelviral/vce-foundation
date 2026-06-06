class TransitionValidator:

    def validate(
        self,
        before,
        after,
        opcode,
    ):

        if opcode.name != "APPEND_EVENT":
            return False

        if after.event_count != before.event_count + 1:
            return False

        if after.last_sequence != before.last_sequence + 1:
            return False

        return True
