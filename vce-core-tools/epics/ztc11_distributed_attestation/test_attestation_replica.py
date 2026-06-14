from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)

from epics.ztc11_distributed_attestation.attestation_replica import (
    AttestationReplica,
)


def test_replica_contains_anchor_reference():

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="hash-001",
        state_root_hash="root-001",
    )

    replica = AttestationReplica(
        replica_id="replica-001",
        anchor=anchor,
        location="witness-001",
    )

    assert replica.anchor.anchor_id == "anchor-001"


def test_replica_serializes():

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="hash-001",
        state_root_hash="root-001",
    )

    replica = AttestationReplica(
        replica_id="replica-001",
        anchor=anchor,
        location="witness-001",
    )

    data = replica.to_dict()

    assert data["replica_id"] == "replica-001"
    assert data["anchor_id"] == "anchor-001"
