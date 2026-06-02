from epics.epic026_recovery.state_pull import (
    StatePull
)

pull = StatePull()

state = pull.pull(
    "http://127.0.0.1:8000"
)

print(
    state["node_id"]
)

print(
    state["sequence_number"]
)

print(
    state["state_hash"]
)

print(
    state["ledger"]
)
