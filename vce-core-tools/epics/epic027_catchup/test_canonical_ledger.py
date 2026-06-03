from epics.epic027_catchup.canonical_ledger import (
    CanonicalLedger
)

selector = CanonicalLedger()

result = selector.select(
    {
        "node-a": [1,2,3,4,5,6],
        "node-b": [1,2,3,4],
        "node-c": [1,2,3,4]
    }
)

print(result)
