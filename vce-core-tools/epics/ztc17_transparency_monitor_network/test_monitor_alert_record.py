from epics.ztc17_transparency_monitor_network.monitor_alert_record import (
    MonitorAlertRecord,
)


def test_alert_contains_monitor_id():

    alert = MonitorAlertRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        reason="root_divergence",
    )

    assert alert.monitor_id == "monitor-001"


def test_alert_contains_registry_and_reason():

    alert = MonitorAlertRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        reason="root_divergence",
    )

    assert alert.registry_id == "registry-a"
    assert alert.reason == "root_divergence"


def test_alert_serializes():

    alert = MonitorAlertRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        reason="root_divergence",
    )

    assert alert.to_dict() == {
        "monitor_id": "monitor-001",
        "registry_id": "registry-a",
        "reason": "root_divergence",
    }
