from epics.epic027_replicated_ledger.replication_verifier import (
    ReplicationVerifier
)


verifier = ReplicationVerifier()

ledgers = verifier.fetch_ledgers(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

for peer, ledger in ledgers.items():
    print(peer, len(ledger))

result = verifier.verify(
    ledgers
)

print(result)
