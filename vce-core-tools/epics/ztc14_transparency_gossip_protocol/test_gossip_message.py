from epics.ztc14_transparency_gossip_protocol.gossip_message import (
    GossipMessage,
)


def test_gossip_message_contains_registry_and_root():

    message = GossipMessage(
        registry_id="registry-a",
        transparency_root="root-001",
        sequence_number=1,
    )

    assert message.registry_id == "registry-a"
    assert message.transparency_root == "root-001"
    assert message.sequence_number == 1


def test_gossip_message_serializes():

    message = GossipMessage(
        registry_id="registry-a",
        transparency_root="root-001",
        sequence_number=1,
    )

    assert message.to_dict() == {
        "registry_id": "registry-a",
        "transparency_root": "root-001",
        "sequence_number": 1,
    }
