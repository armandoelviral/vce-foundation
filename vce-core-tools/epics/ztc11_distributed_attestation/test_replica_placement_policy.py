from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)

from epics.ztc11_distributed_attestation.replica_placement_policy import (
    ReplicaPlacementPolicy,
)


def test_accepts_replicas_across_required_locations():

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

    assert ReplicaPlacementPolicy.allow(
        replicas=replicas,
        minimum_replicas=3,
        minimum_locations=3,
    )


def test_rejects_insufficient_replica_count():

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
        )
    ]

    assert not ReplicaPlacementPolicy.allow(
        replicas=replicas,
        minimum_replicas=3,
        minimum_locations=1,
    )


def test_rejects_insufficient_location_diversity():

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
            location="aws",
        ),
        AttestationReplica(
            replica_id="replica-003",
            anchor=anchor,
            location="aws",
        ),
    ]

    assert not ReplicaPlacementPolicy.allow(
        replicas=replicas,
        minimum_replicas=3,
        minimum_locations=3,
    )
