from epics.ztc19_governance_ledger.governance_hash_chain import (
    GovernanceHashChain,
)

from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)


def test_first_entry_uses_genesis_hash():

    chain = GovernanceHashChain()

    entry = GovernanceLedgerEntry(
        sequence=1,
        event_id="event-001",
    )

    record = chain.append(entry)

    assert record["previous_hash"] == "GENESIS"


def test_second_entry_links_to_first_hash():

    chain = GovernanceHashChain()

    first = chain.append(
        GovernanceLedgerEntry(
            sequence=1,
            event_id="event-001",
        )
    )

    second = chain.append(
        GovernanceLedgerEntry(
            sequence=2,
            event_id="event-002",
        )
    )

    assert second["previous_hash"] == first["current_hash"]


def test_hash_changes_with_entry():

    chain = GovernanceHashChain()

    first = chain.append(
        GovernanceLedgerEntry(
            sequence=1,
            event_id="event-001",
        )
    )

    second = chain.append(
        GovernanceLedgerEntry(
            sequence=2,
            event_id="event-002",
        )
    )

    assert first["current_hash"] != second["current_hash"]
