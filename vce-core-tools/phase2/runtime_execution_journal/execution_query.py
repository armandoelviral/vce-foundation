class ExecutionQuery:

    def __init__(
        self,
        journal,
    ):

        self.journal = journal

    def by_opcode(
        self,
        opcode: str,
    ):

        return [
            record
            for record
            in self.journal.all()
            if record.opcode == opcode
        ]
