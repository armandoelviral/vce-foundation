from epics.epic027_replicated_ledger.broadcast_append import (
    BroadcastAppend
)

broadcast = BroadcastAppend()

results = broadcast.broadcast(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ],
    {
        "sequence": 99,
        "event": "CLUSTER_REPLICATION"
    }
)

for result in results:

    print(result)
