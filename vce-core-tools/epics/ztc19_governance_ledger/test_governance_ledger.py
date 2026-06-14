from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)

from epics.ztc19_governance_ledger.governance_ledger import (
    GovernanceLedger,
)


def test_ledger_stores_entry():

    ledger = GovernanceLedger()

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    ledger.append(entry)

    assert ledger.count() == 1


def test_ledger_returns_entries():

    ledger = GovernanceLedger()

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    ledger.append(entry)

    entries = ledger.all()

    assert len(entries) == 1
    assert entries[0].event_id == "event-001"


def test_ledger_starts_empty():

    ledger = GovernanceLedger()

    assert ledger.count() == 0
