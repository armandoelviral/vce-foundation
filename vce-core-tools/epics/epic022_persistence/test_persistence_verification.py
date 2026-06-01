import os

from epics.epic022_persistence.persistent_ledger import (
    PersistentLedger
)

from epics.epic022_persistence.persistence_verification import (
    PersistenceVerification
)


db_path = "verification_test.db"

if os.path.exists(
    db_path
):
    os.remove(
        db_path
    )


ledger = PersistentLedger(
    db_path
)

ledger.append(
    "CHECKPOINT",
    {
        "state_hash":
            "verified123"
    }
)


result = (
    PersistenceVerification()
).verify(
    db_path
)


print(
    result[
        "consistent"
    ]
)

print(
    result[
        "recovered"
    ]
)

print(
    result[
        "verified"
    ]
)
