import os

from epics.epic028_durable_node_ledger.node_ledger import (
    NodeLedger
)


db_path = "test_node_ledger.db"

if os.path.exists(db_path):
    os.remove(db_path)


ledger = NodeLedger(db_path)

ledger.append(
    {
        "sequence": 1,
        "event": "BOOTSTRAP"
    }
)

ledger.append(
    {
        "sequence": 2,
        "event": "REMOTE_APPEND"
    }
)

reloaded = NodeLedger(db_path)

print(reloaded.count())
print(reloaded.all())
