import os

from epics.epic028_durable_node_ledger.node_ledger import (
    NodeLedger
)

db_path = "idempotent_test.db"

if os.path.exists(
    db_path
):
    os.remove(
        db_path
    )

ledger = NodeLedger(
    db_path
)

print(
    ledger.append(
        {
            "sequence": 1,
            "event": "BOOTSTRAP"
        }
    )
)

print(
    ledger.append(
        {
            "sequence": 1,
            "event": "BOOTSTRAP"
        }
    )
)

print(
    ledger.count()
)
