from epics.epic028_durable_node_ledger.node_ledger import (
    NodeLedger
)

ledger = NodeLedger(
    "repair_test.db"
)

ledger.replace_all(
    [
        {
            "sequence": 1,
            "event": "BOOTSTRAP"
        },
        {
            "sequence": 2,
            "event": "RECOVERED"
        },
        {
            "sequence": 3,
            "event": "RECOVERED"
        }
    ]
)

print(
    ledger.count()
)

print(
    ledger.all()
)
