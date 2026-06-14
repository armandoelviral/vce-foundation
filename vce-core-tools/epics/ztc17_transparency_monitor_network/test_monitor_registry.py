from epics.ztc17_transparency_monitor_network.transparency_monitor_node import (
    TransparencyMonitorNode,
)

from epics.ztc17_transparency_monitor_network.monitor_registry import (
    MonitorRegistry,
)


def test_registry_stores_monitor():

    registry = MonitorRegistry()

    monitor = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    registry.add(monitor)

    assert registry.count() == 1


def test_registry_reports_known_monitor():

    registry = MonitorRegistry()

    monitor = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    registry.add(monitor)

    assert registry.exists(
        "monitor-001"
    )


def test_registry_returns_false_for_unknown_monitor():

    registry = MonitorRegistry()

    assert not registry.exists(
        "monitor-999"
    )
