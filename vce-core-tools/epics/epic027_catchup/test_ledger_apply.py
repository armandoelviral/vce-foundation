from epics.epic027_catchup.ledger_apply import (
    LedgerApply
)

apply = LedgerApply()

print(
    "BEFORE",
    len(
        apply.current()
    )
)

canonical_ledger = [
    {
        "sequence": 1,
        "event": "BOOTSTRAP"
    },
    {
        "sequence": 2,
        "event": "ATTESTATION"
    },
    {
        "sequence": 3,
        "event": "REMOTE_APPEND"
    },
    {
        "sequence": 99,
        "event": "CLUSTER_REPLICATION"
    }
]

apply.apply(
    canonical_ledger
)

print(
    "AFTER",
    len(
        apply.current()
    )
)

print(
    apply.current()
)
