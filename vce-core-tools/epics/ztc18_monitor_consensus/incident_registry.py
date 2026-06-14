from typing import List

from epics.ztc18_monitor_consensus.incident_declaration import (
    IncidentDeclaration,
)


class IncidentRegistry:

    def __init__(self):

        self._incidents: List[
            IncidentDeclaration
        ] = []

    def add(
        self,
        incident: IncidentDeclaration,
    ) -> None:

        self._incidents.append(
            incident
        )

    def all(
        self,
    ):

        return list(
            self._incidents
        )

    def count(
        self,
    ) -> int:

        return len(
            self._incidents
        )
