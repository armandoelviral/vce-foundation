from epics.epic025_cluster_runtime.peer_discovery import (
    PeerDiscovery
)

discovery = PeerDiscovery()

cluster = discovery.discover(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ]
)

for peer in cluster:
    print(peer)
