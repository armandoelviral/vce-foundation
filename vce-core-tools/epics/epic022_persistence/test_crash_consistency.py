import os

from epics.epic022_persistence.persistent_ledger import (
    PersistentLedger
)

from epics.epic022_persistence.crash_consistency import (
    CrashConsistencyChecker
)


db_path = "crash_test.db"

if os.path.exists(db_path):
    os.remove(db_path)


ledger = PersistentLedger(
    db_path
)

ledger.append(
    "CHECKPOINT",
    {
        "hash": "abc123"
    }
)

checker = CrashConsistencyChecker(
    db_path
)

result = checker.verify()

print(
    result["consistent"]
)
