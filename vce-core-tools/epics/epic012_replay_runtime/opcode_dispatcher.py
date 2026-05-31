class OpcodeDispatcher:

    def dispatch(self, state, event):

        opcode = event["opcode"]
        payload = event["payload"]

        if opcode == "APPEND_EVIDENCE":
            state.append_event(
                f"APPEND_EVIDENCE:{payload}"
            )

        elif opcode == "REGISTER_ARTIFACT":
            state.append_event(
                f"REGISTER_ARTIFACT:{payload}"
            )

        elif opcode == "SEAL_SNAPSHOT":
            state.append_event(
                f"SEAL_SNAPSHOT:{payload}"
            )

        else:
            raise ValueError(
                f"UNKNOWN_OPCODE: {opcode}"
            )

        return state
