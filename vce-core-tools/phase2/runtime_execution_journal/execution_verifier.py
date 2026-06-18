from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)


class ExecutionVerifier:

    @staticmethod
    def verify(
        record: ExecutionRecord,
        expected_output: str,
    ) -> bool:

        if not record.output_data:
            return False

        return (
            record.output_data
            == expected_output
        )
