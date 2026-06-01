from epics.epic019_networked_trust.peer_discovery import (
    PeerDiscovery
)


network = PeerDiscovery()


network.register(
    "node-A",
    "localhost:1001"
)


network.register(
    "node-B",
    "localhost:1002"
)


print(
    len(
        network.active_peers()
    )
)


network.remove(
    "node-B"
)


print(
    len(
        network.active_peers()
    )
)
