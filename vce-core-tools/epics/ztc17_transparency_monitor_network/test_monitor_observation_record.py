from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)


def test_observation_contains_monitor_id():

    record = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    assert record.monitor_id == "monitor-001"


def test_observation_contains_registry_and_root():

    record = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    assert record.registry_id == "registry-a"
    assert record.observed_root == "root-001"


def test_observation_serializes():

    record = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    assert record.to_dict() == {
        "monitor_id": "monitor-001",
        "registry_id": "registry-a",
        "observed_root": "root-001",
    }
