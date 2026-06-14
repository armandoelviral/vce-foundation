from epics.ztc17_transparency_monitor_network.transparency_monitor_node import (
    TransparencyMonitorNode,
)


def test_monitor_node_contains_identity():

    node = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    assert node.monitor_id == "monitor-001"


def test_monitor_node_contains_endpoint():

    node = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    assert node.endpoint == "https://monitor-001.example"


def test_monitor_node_serializes():

    node = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    assert node.to_dict() == {
        "monitor_id": "monitor-001",
        "endpoint": "https://monitor-001.example",
    }
