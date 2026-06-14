from typing import List

from epics.ztc17_transparency_monitor_network.monitor_observation_record import (
    MonitorObservationRecord,
)


class ObservationRegistry:

    def __init__(self):

        self._observations: List[
            MonitorObservationRecord
        ] = []

    def add(
        self,
        observation: MonitorObservationRecord,
    ) -> None:

        self._observations.append(
            observation
        )

    def all(
        self,
    ) -> List[MonitorObservationRecord]:

        return list(
            self._observations
        )

    def count(
        self,
    ) -> int:

        return len(
            self._observations
        )
