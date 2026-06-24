from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)


def test_consumption_creation():
    record = ReserveConsumptionRecord(
        consumption_id="consumption.001",
        reserve_id="reserve.001",
        consumed_amount=40,
        reason="insurance payout",
    )

    assert record.consumption_id == "consumption.001"
    assert record.reserve_id == "reserve.001"
    assert record.consumed_amount == 40
    assert record.reason == "insurance payout"


def test_rejects_empty_consumption_id():
    try:
        ReserveConsumptionRecord(
            consumption_id="",
            reserve_id="reserve.001",
            consumed_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "consumption_id" in str(exc)


def test_rejects_non_positive_amount():
    try:
        ReserveConsumptionRecord(
            consumption_id="consumption.001",
            reserve_id="reserve.001",
            consumed_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "consumed_amount" in str(exc)
