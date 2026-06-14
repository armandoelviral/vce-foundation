from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)


def test_entry_contains_sequence():

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    assert entry.sequence == 1


def test_entry_contains_event_id():

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    assert entry.event_id == "event-001"


def test_entry_serializes():

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    assert entry.to_dict() == {
        "sequence": 1,
        "event_id": "event-001",
    }
