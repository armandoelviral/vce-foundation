from epics.ztc17_transparency_monitor_network.transparency_monitor_node import (
    TransparencyMonitorNode,
)

from epics.ztc17_transparency_monitor_network.monitor_registry import (
    MonitorRegistry,
)

from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)

from epics.ztc17_transparency_monitor_network.observation_registry import (
    ObservationRegistry,
)

from epics.ztc17_transparency_monitor_network.monitor_divergence_detector import (
    MonitorDivergenceDetector,
)

from epics.ztc17_transparency_monitor_network.monitor_divergence_report import (
    MonitorDivergenceReport,
)

from epics.ztc17_transparency_monitor_network.monitor_alert_record import (
    MonitorAlertRecord,
)


def test_end_to_end_transparency_monitor_flow():

    monitor_registry = MonitorRegistry()

    monitor_a = TransparencyMonitorNode(
        monitor_id="monitor-001",
        endpoint="https://monitor-001.example",
    )

    monitor_b = TransparencyMonitorNode(
        monitor_id="monitor-002",
        endpoint="https://monitor-002.example",
    )

    monitor_registry.add(monitor_a)
    monitor_registry.add(monitor_b)

    assert monitor_registry.count() == 2

    observation_registry = ObservationRegistry()

    observation_a = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    observation_b = MonitorObservationRecord(
        monitor_id="monitor-002",
        registry_id="registry-a",
        observed_root="root-002",
    )

    observation_registry.add(observation_a)
    observation_registry.add(observation_b)

    divergent = MonitorDivergenceDetector.detect(
        observation_a,
        observation_b,
    )

    report = MonitorDivergenceReport(
        monitor_a="monitor-001",
        monitor_b="monitor-002",
        registry_id="registry-a",
        divergent=divergent,
    )

    alert = MonitorAlertRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        reason="root_divergence",
    )

    assert divergent is True
    assert report.divergent is True
    assert alert.reason == "root_divergence"
