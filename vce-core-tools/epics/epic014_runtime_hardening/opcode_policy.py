class OpcodePolicy:

    ALLOWED_OPCODES = {
        "APPEND_EVIDENCE",
        "REGISTER_ARTIFACT",
        "SEAL_SNAPSHOT",
    }


    def validate(self, event):

        opcode = event.get(
            "opcode"
        )

        return opcode in self.ALLOWED_OPCODES


    def validate_stream(self, events):

        for event in events:

            if not self.validate(event):
                return False

        return True
