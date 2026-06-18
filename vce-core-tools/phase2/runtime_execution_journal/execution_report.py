class ExecutionReport:

    def __init__(
        self,
        records,
    ):

        self.records = records

    def total_executions(
        self,
    ) -> int:

        return len(
            self.records
        )

    def opcodes(
        self,
    ):

        return [
            record.opcode
            for record in self.records
        ]

    def to_dict(
        self,
    ):

        return {
            "total_executions":
                self.total_executions(),
            "opcodes":
                self.opcodes(),
        }
