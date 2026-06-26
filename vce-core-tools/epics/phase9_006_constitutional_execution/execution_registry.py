from epics.phase9_006_constitutional_execution.execution_record import (
    ExecutionRecord,
)


class ExecutionRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: ExecutionRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
