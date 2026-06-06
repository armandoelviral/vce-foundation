from epics.epic013_external_trust.immutable_ledger import (
    ImmutableLedgerStore,
)


def test_ledger_links_records_with_hash_chain():

    ledger = ImmutableLedgerStore()

    record_1 = ledger.append(
        {
            "status": "COMMITTED",
            "state_hash": "abc123",
            "sequence_number": 3,
        }
    )

    record_2 = ledger.append(
        {
            "status": "COMMITTED",
            "state_hash": "def456",
            "sequence_number": 4,
        }
    )

    assert (
        record_2["previous_hash"]
        == record_1["current_hash"]
    )


def test_ledger_detects_tampering():

    ledger = ImmutableLedgerStore()

    ledger.append(
        {
            "status": "COMMITTED",
            "state_hash": "abc123",
            "sequence_number": 3,
        }
    )

    ledger.append(
        {
            "status": "COMMITTED",
            "state_hash": "def456",
            "sequence_number": 4,
        }
    )

    assert ledger.verify() is True

    ledger.records[0]["entry"]["state_hash"] = "TAMPERED"

    assert ledger.verify() is False
