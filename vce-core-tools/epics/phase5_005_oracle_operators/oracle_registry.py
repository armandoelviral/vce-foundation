from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)


class OracleRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: OracleRecord):
        if record.oracle_id in self._ids:
            raise ValueError("duplicate oracle")

        self._records.append(record)
        self._ids.add(record.oracle_id)

    def records(self):
        return list(self._records)
