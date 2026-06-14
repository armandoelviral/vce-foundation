from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)

from epics.ztc11_distributed_attestation.replica_registry import (
    ReplicaRegistry,
)


def test_registry_stores_replica():

    registry = ReplicaRegistry()

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="hash-001",
        state_root_hash="root-001",
    )

    replica = AttestationReplica(
        replica_id="replica-001",
        anchor=anchor,
        location="aws",
    )

    registry.register(replica)

    assert registry.count() == 1


def test_registry_returns_replicas():

    registry = ReplicaRegistry()

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="hash-001",
        state_root_hash="root-001",
    )

    replica = AttestationReplica(
        replica_id="replica-001",
        anchor=anchor,
        location="gcp",
    )

    registry.register(replica)

    replicas = registry.all()

    assert len(replicas) == 1
    assert replicas[0].location == "gcp"
