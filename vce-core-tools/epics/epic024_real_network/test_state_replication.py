from epics.epic024_real_network.state_replication import (
    StateReplication
)


replication = StateReplication()


state = replication.fetch_state(
    "http://127.0.0.1:8000"
)


comparison = replication.compare(
    "abc123",
    state["state_hash"]
)


print(
    state["node_id"]
)

print(
    state["sequence_number"]
)

print(
    comparison["in_sync"]
)

print(
    replication.sync_decision(
        "abc123",
        state["state_hash"]
    )
)
