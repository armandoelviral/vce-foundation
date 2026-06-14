from epics.ztc19_governance_ledger.governance_hash_chain import (
    GovernanceHashChain,
)

from epics.ztc19_governance_ledger.governance_chain_verifier import (
    GovernanceChainVerifier,
)

from epics.ztc19_governance_ledger.governance_ledger_entry import (
    GovernanceLedgerEntry,
)


def test_accepts_valid_chain():

    chain = GovernanceHashChain()

    chain.append(
        GovernanceLedgerEntry(
            sequence=1,
            event_id="event-001",
        )
    )

    chain.append(
        GovernanceLedgerEntry(
            sequence=2,
            event_id="event-002",
        )
    )

    verifier = GovernanceChainVerifier()

    assert verifier.verify(
        chain._records
    )


def test_detects_tampered_chain():

    chain = GovernanceHashChain()

    chain.append(
        GovernanceLedgerEntry(
            sequence=1,
            event_id="event-001",
        )
    )

    chain.append(
        GovernanceLedgerEntry(
            sequence=2,
            event_id="event-002",
        )
    )

    chain._records[1]["previous_hash"] = (
        "tampered"
    )

    verifier = GovernanceChainVerifier()

    assert not verifier.verify(
        chain._records
    )
