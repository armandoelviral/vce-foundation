from epics.ztc13_transparency_federation.federated_transparency_proof import (
    FederatedTransparencyProof,
)


def test_proof_contains_anchor():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert proof.anchor_id == "anchor-001"


def test_proof_contains_source_registry():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert proof.source_registry == "registry-a"


def test_proof_contains_target_registry():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert proof.target_registry == "registry-b"


def test_proof_serializes():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert proof.to_dict() == {
        "anchor_id": "anchor-001",
        "source_registry": "registry-a",
        "target_registry": "registry-b",
    }
