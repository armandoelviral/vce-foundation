from epics.epic026_recovery.state_selector import (
    StateSelector
)

selector = StateSelector()

states = [
    {
        "node_id": "node-a",
        "sequence_number": 42,
        "state_hash": "abc123"
    },
    {
        "node_id": "node-b",
        "sequence_number": 42,
        "state_hash": "abc123"
    },
    {
        "node_id": "node-c",
        "sequence_number": 15,
        "state_hash": "old999"
    }
]

selected = selector.select(
    states
)

print(selected)
