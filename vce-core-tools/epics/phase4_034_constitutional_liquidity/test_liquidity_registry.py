from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_registry import (
    LiquidityRegistry,
)


def test_registry_stores_record():
    registry = LiquidityRegistry()

    record = LiquidityRecord(
        liquidity_id="liq.001",
        source_id="treasury.001",
        liquidity_amount=100,
        purpose="response",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_rejects_duplicate_record():
    registry = LiquidityRegistry()

    record = LiquidityRecord(
        liquidity_id="liq.001",
        source_id="treasury.001",
        liquidity_amount=100,
        purpose="response",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate liquidity" in str(exc)


def test_returns_copy():
    registry = LiquidityRegistry()

    record = LiquidityRecord(
        liquidity_id="liq.001",
        source_id="treasury.001",
        liquidity_amount=100,
        purpose="response",
    )

    registry.add(record)

    items = registry.records()
    items.clear()

    assert len(registry.records()) == 1
