from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)

from epics.ztc11_distributed_attestation.replica_registry import (
    ReplicaRegistry,
)

from epics.ztc11_distributed_attestation.replica_placement_policy import (
    ReplicaPlacementPolicy,
)

from epics.ztc11_distributed_attestation.replica_recovery import (
    ReplicaRecovery,
)


def test_end_to_end_distributed_attestation_flow():

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="hash-001",
        state_root_hash="root-001",
    )

    replicas = [
        AttestationReplica(
            replica_id="replica-001",
            anchor=anchor,
            location="aws",
        ),
        AttestationReplica(
            replica_id="replica-002",
            anchor=anchor,
            location="gcp",
        ),
        AttestationReplica(
            replica_id="replica-003",
            anchor=anchor,
            location="azure",
        ),
    ]

    registry = ReplicaRegistry()

    for replica in replicas:
        registry.register(replica)

    placement_ok = ReplicaPlacementPolicy.allow(
        replicas=registry.all(),
        minimum_replicas=3,
        minimum_locations=3,
    )

    recovery_required = ReplicaRecovery.required(
        replica_count=registry.count(),
        minimum_replicas=3,
    )

    assert placement_ok is True
    assert recovery_required is False
