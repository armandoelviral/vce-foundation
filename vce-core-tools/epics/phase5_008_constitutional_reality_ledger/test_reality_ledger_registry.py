from epics.phase5_008_constitutional_reality_ledger.reality_ledger_record import (
    RealityLedgerRecord,
)
from epics.phase5_008_constitutional_reality_ledger.reality_ledger_registry import (
    RealityLedgerRegistry,
)


def test_registry_adds_record():
    registry = RealityLedgerRegistry()

    record = RealityLedgerRecord(
        "ledger.001",
        "claim.001",
        "consensus.001",
    )

    registry.add(record)

    assert registry.records() == [record]
