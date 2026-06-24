from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


def test_treasury_record_creation():
    record = TreasuryRecord(
        treasury_id="treasury.001",
        authority_id="treasury.council",
        allocation_amount=100,
        reserve_reference="reserve.001",
    )

    assert record.treasury_id == "treasury.001"
    assert record.authority_id == "treasury.council"
    assert record.allocation_amount == 100
    assert record.reserve_reference == "reserve.001"


def test_rejects_empty_treasury_id():
    try:
        TreasuryRecord(
            treasury_id="",
            authority_id="treasury.council",
            allocation_amount=100,
            reserve_reference="reserve.001",
        )
        assert False
    except ValueError as exc:
        assert "treasury_id" in str(exc)


def test_rejects_non_positive_allocation():
    try:
        TreasuryRecord(
            treasury_id="treasury.001",
            authority_id="treasury.council",
            allocation_amount=0,
            reserve_reference="reserve.001",
        )
        assert False
    except ValueError as exc:
        assert "allocation_amount" in str(exc)
