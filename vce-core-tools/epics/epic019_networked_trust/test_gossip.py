from epics.epic019_networked_trust.gossip import (
    GossipProtocol
)


gossip = GossipProtocol()


result = gossip.propagate(
    [
        "node-A",
        "node-B",
        "node-C"
    ],
    {
        "artifact":
            "verified-build-001"
    }
)


print(
    result[
        "propagated"
    ]
)


print(
    result[
        "peers_reached"
    ]
)
