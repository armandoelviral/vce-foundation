from epics.ztc13_transparency_federation.federated_transparency_proof import (
    FederatedTransparencyProof,
)

from epics.ztc13_transparency_federation.federated_transparency_verifier import (
    FederatedTransparencyVerifier,
)


def test_accepts_complete_federated_proof():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert FederatedTransparencyVerifier.verify(proof)


def test_rejects_missing_anchor_id():

    proof = FederatedTransparencyProof(
        anchor_id="",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert not FederatedTransparencyVerifier.verify(proof)


def test_rejects_missing_source_registry():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="",
        target_registry="registry-b",
    )

    assert not FederatedTransparencyVerifier.verify(proof)


def test_rejects_missing_target_registry():

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="",
    )

    assert not FederatedTransparencyVerifier.verify(proof)
