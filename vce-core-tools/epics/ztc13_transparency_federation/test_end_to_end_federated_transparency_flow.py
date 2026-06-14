from epics.ztc13_transparency_federation.transparency_anchor import (
    TransparencyAnchor,
)

from epics.ztc13_transparency_federation.transparency_registry import (
    TransparencyRegistry,
)

from epics.ztc13_transparency_federation.federated_transparency_registry import (
    FederatedTransparencyRegistry,
)

from epics.ztc13_transparency_federation.federated_transparency_proof import (
    FederatedTransparencyProof,
)

from epics.ztc13_transparency_federation.federated_transparency_verifier import (
    FederatedTransparencyVerifier,
)


def test_end_to_end_federated_transparency_flow():

    registry = TransparencyRegistry()

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    registry.add(anchor)

    federation = FederatedTransparencyRegistry(
        [registry]
    )

    assert federation.exists(
        "anchor-001"
    )

    proof = FederatedTransparencyProof(
        anchor_id="anchor-001",
        source_registry="registry-a",
        target_registry="registry-b",
    )

    assert FederatedTransparencyVerifier.verify(
        proof
    )
