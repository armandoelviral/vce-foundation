from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)


class ExecutionJournal:

    def __init__(self):

        self._records = {}

    def append(
        self,
        record: ExecutionRecord,
    ) -> None:

        self._records[
            record.execution_id
        ] = record

    def get(
        self,
        execution_id: str,
    ):

        return self._records.get(
            execution_id
        )

    def all(self):

        return list(
            self._records.values()
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
