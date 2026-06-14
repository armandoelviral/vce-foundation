from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)


def test_anchor_contains_attestation_identity():

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="attestation-hash-001",
        state_root_hash="state-root-001",
    )

    assert anchor.anchor_id == "anchor-001"
    assert anchor.attestation_hash == "attestation-hash-001"
    assert anchor.state_root_hash == "state-root-001"


def test_anchor_serializes():

    anchor = AttestationAnchor(
        anchor_id="anchor-001",
        attestation_hash="attestation-hash-001",
        state_root_hash="state-root-001",
    )

    assert anchor.to_dict() == {
        "anchor_id": "anchor-001",
        "attestation_hash": "attestation-hash-001",
        "state_root_hash": "state-root-001",
    }
