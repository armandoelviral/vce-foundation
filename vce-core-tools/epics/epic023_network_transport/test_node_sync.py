from epics.epic023_network_transport.node_sync import (
    NodeSynchronization
)


sync = NodeSynchronization()


same = sync.compare(
    "abc123",
    "abc123"
)


different = sync.compare(
    "abc123",
    "xyz999"
)


print(
    same["in_sync"]
)


print(
    different["in_sync"]
)


print(
    sync.synchronize(
        "abc123",
        "xyz999"
    )["action"]
)
