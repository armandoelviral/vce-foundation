from epics.epic024_real_network.state_replication import (
    StateReplication
)

replication = StateReplication()

nodes = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002"
]

for node in nodes:

    state = replication.fetch_state(node)

    print(
        state["node_id"],
        state["state_hash"]
    )
