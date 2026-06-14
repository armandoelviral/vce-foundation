from typing import List

from epics.ztc17_transparency_monitor_network.transparency_monitor_node import (
    TransparencyMonitorNode,
)


class MonitorRegistry:

    def __init__(self):

        self._monitors: List[
            TransparencyMonitorNode
        ] = []

    def add(
        self,
        monitor: TransparencyMonitorNode,
    ) -> None:

        self._monitors.append(
            monitor
        )

    def count(
        self,
    ) -> int:

        return len(
            self._monitors
        )

    def exists(
        self,
        monitor_id: str,
    ) -> bool:

        return any(
            monitor.monitor_id == monitor_id
            for monitor in self._monitors
        )
