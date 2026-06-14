from epics.ztc11_distributed_attestation.replica_recovery import (
    ReplicaRecovery,
)


def test_recovery_not_required():

    assert not ReplicaRecovery.required(
        replica_count=3,
        minimum_replicas=3,
    )


def test_recovery_required():

    assert ReplicaRecovery.required(
        replica_count=2,
        minimum_replicas=3,
    )
