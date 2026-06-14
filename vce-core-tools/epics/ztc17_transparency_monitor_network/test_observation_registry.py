from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)

from epics.ztc17_transparency_monitor_network.observation_registry import (
    ObservationRegistry,
)


def test_registry_stores_observation():

    registry = ObservationRegistry()

    observation = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    registry.add(observation)

    assert registry.count() == 1


def test_registry_returns_observations():

    registry = ObservationRegistry()

    observation = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    registry.add(observation)

    observations = registry.all()

    assert len(observations) == 1
    assert observations[0].monitor_id == "monitor-001"


def test_registry_starts_empty():

    registry = ObservationRegistry()

    assert registry.count() == 0
