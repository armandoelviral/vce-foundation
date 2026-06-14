from epics.ztc14_transparency_gossip_protocol.gossip_message import (
    GossipMessage,
)

from epics.ztc14_transparency_gossip_protocol.gossip_registry import (
    GossipRegistry,
)


def test_registry_stores_message():

    registry = GossipRegistry()

    message = GossipMessage(
        registry_id="registry-a",
        transparency_root="root-001",
        sequence_number=1,
    )

    registry.add(message)

    assert registry.count() == 1


def test_registry_returns_messages():

    registry = GossipRegistry()

    message = GossipMessage(
        registry_id="registry-a",
        transparency_root="root-001",
        sequence_number=1,
    )

    registry.add(message)

    stored = registry.all()

    assert len(stored) == 1
    assert stored[0].registry_id == "registry-a"


def test_registry_starts_empty():

    registry = GossipRegistry()

    assert registry.count() == 0
