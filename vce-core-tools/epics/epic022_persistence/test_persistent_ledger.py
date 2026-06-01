from epics.epic022_persistence.persistent_ledger import (
    PersistentLedger
)


ledger = PersistentLedger(
    "test_ledger.db"
)


ledger.append(
    "CHECKPOINT",
    {
        "hash": "abc123"
    }
)


ledger.append(
    "ATTESTATION",
    {
        "artifact": "runtime"
    }
)


print(
    ledger.count()
)
