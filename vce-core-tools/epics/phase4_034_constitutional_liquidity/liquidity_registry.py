from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


class LiquidityRegistry:
    def __init__(self):
        self._records = []
        self._ids = set()

    def add(self, record: LiquidityRecord):
        if record.liquidity_id in self._ids:
            raise ValueError("duplicate liquidity")

        self._records.append(record)
        self._ids.add(record.liquidity_id)

    def records(self):
        return list(self._records)
