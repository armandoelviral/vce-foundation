from epics.phase4_033_constitutional_treasury.treasury_disbursement import (
    TreasuryDisbursementRecord,
)


def test_disbursement_creation():
    record = TreasuryDisbursementRecord(
        disbursement_id="disbursement.001",
        treasury_id="treasury.001",
        disbursement_amount=40,
        purpose="insurance support",
    )

    assert record.disbursement_id == "disbursement.001"
    assert record.treasury_id == "treasury.001"
    assert record.disbursement_amount == 40


def test_rejects_empty_disbursement_id():
    try:
        TreasuryDisbursementRecord(
            disbursement_id="",
            treasury_id="treasury.001",
            disbursement_amount=40,
            purpose="invalid",
        )
        assert False
    except ValueError as exc:
        assert "disbursement_id" in str(exc)


def test_rejects_non_positive_disbursement_amount():
    try:
        TreasuryDisbursementRecord(
            disbursement_id="d1",
            treasury_id="t1",
            disbursement_amount=0,
            purpose="invalid",
        )
        assert False
    except ValueError as exc:
        assert "disbursement_amount" in str(exc)
