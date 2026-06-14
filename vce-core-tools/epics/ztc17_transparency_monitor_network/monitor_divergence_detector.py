from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)


class MonitorDivergenceDetector:

    @staticmethod
    def detect(
        observation_a: MonitorObservationRecord,
        observation_b: MonitorObservationRecord,
    ) -> bool:

        return (
            observation_a.observed_root
            != observation_b.observed_root
        )
