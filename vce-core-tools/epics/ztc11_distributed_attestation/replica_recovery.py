class ReplicaRecovery:

    @staticmethod
    def required(
        replica_count: int,
        minimum_replicas: int,
    ) -> bool:

        return replica_count < minimum_replicas
