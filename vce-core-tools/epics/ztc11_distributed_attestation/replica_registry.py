from typing import List

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)


class ReplicaRegistry:

    def __init__(self):

        self._replicas: List[
            AttestationReplica
        ] = []

    def register(
        self,
        replica: AttestationReplica,
    ) -> None:

        self._replicas.append(
            replica
        )

    def all(
        self,
    ) -> List[AttestationReplica]:

        return list(
            self._replicas
        )

    def count(
        self,
    ) -> int:

        return len(
            self._replicas
        )
