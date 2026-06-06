class OpcodeRegistry:

    def __init__(self):
        self._handlers = {}

    def register(
        self,
        opcode,
        handler,
    ):
        self._handlers[opcode] = handler

    def execute(
        self,
        opcode,
        payload,
    ):
        if opcode not in self._handlers:
            return False

        return self._handlers[opcode](
            payload
        )
