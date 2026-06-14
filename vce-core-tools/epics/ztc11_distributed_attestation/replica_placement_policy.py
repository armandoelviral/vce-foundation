from typing import Iterable

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)


class ReplicaPlacementPolicy:

    @staticmethod
    def allow(
        replicas: Iterable[AttestationReplica],
        minimum_replicas: int,
        minimum_locations: int,
    ) -> bool:

        replica_list = list(replicas)

        locations = {
            replica.location
            for replica in replica_list
        }

        return (
            len(replica_list) >= minimum_replicas
            and len(locations) >= minimum_locations
        )
