from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)


def test_reality_ledger_record_creation():
    record = RealityLedgerRecord(
        ledger_id="ledger.001",
        claim_id="claim.001",
        consensus_id="consensus.001",
    )

    assert record.ledger_id == "ledger.001"


def test_rejects_empty_ledger_id():
    try:
        RealityLedgerRecord(
            "",
            "claim.001",
            "consensus.001",
        )
        assert False
    except ValueError as exc:
        assert "ledger_id" in str(exc)
