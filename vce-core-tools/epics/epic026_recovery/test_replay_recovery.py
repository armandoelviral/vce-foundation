from epics.epic026_recovery.replay_recovery import (
    ReplayRecovery
)

ledger = [
    {
        "sequence": 1,
        "event": "BOOTSTRAP"
    },
    {
        "sequence": 2,
        "event": "ATTESTATION"
    }
]

replay = ReplayRecovery()

state = replay.rebuild(
    ledger
)

print(state)
