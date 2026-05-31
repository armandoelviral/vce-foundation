from immutable_ledger import ImmutableLedgerStore


ledger = ImmutableLedgerStore()

record_1 = ledger.append(
    {
        "status": "COMMITTED",
        "state_hash": "abc123",
        "sequence_number": 3
    }
)

record_2 = ledger.append(
    {
        "status": "COMMITTED",
        "state_hash": "def456",
        "sequence_number": 4
    }
)

print(
    record_2["previous_hash"] ==
    record_1["current_hash"]
)

print(
    ledger.verify()
)

ledger.records[0]["entry"]["state_hash"] = "TAMPERED"

print(
    ledger.verify()
)
