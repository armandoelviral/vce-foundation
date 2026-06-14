from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)

from epics.ztc17_transparency_monitor_network.monitor_divergence_detector import (
    MonitorDivergenceDetector,
)


def test_accepts_matching_roots():

    observation_a = MonitorObservationRecord(
        monitor_id="monitor-001",
        registry_id="registry-a",
        observed_root="root-001",
    )

    observation_b = MonitorObservationRecord(
        monitor_id="monitor-002",
        registry_id="registry-a",
        observed_root="root-001",
    )

    assert not MonitorDivergenceDetector.detect(
        observation_a,
        observation_b,
    )


def test_detects_divergent_roots():

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

    assert MonitorDivergenceDetector.detect(
        observation_a,
        observation_b,
    )
