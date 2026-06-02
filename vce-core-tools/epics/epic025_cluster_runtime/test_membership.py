from epics.epic025_cluster_runtime.peer_discovery import (
    PeerDiscovery
)

from epics.epic025_cluster_runtime.membership import (
    MembershipView
)

discovery = PeerDiscovery()

membership = MembershipView()

cluster = discovery.discover(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

membership.update(
    cluster
)

print(
    membership.alive_nodes()
)

print(
    membership.dead_nodes()
)
