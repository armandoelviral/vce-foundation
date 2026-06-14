from epics.ztc17_transparency_monitor_network.monitor_divergence_report import (
    MonitorDivergenceReport,
)


def test_report_contains_monitor_ids():

    report = MonitorDivergenceReport(
        monitor_a="monitor-001",
        monitor_b="monitor-002",
        registry_id="registry-a",
        divergent=True,
    )

    assert report.monitor_a == "monitor-001"
    assert report.monitor_b == "monitor-002"


def test_report_contains_registry_and_status():

    report = MonitorDivergenceReport(
        monitor_a="monitor-001",
        monitor_b="monitor-002",
        registry_id="registry-a",
        divergent=True,
    )

    assert report.registry_id == "registry-a"
    assert report.divergent is True


def test_report_serializes():

    report = MonitorDivergenceReport(
        monitor_a="monitor-001",
        monitor_b="monitor-002",
        registry_id="registry-a",
        divergent=False,
    )

    assert report.to_dict() == {
        "monitor_a": "monitor-001",
        "monitor_b": "monitor-002",
        "registry_id": "registry-a",
        "divergent": False,
    }
