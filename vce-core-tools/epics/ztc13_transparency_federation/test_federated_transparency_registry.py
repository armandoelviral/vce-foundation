from epics.ztc13_transparency_federation.transparency_anchor import (
    TransparencyAnchor,
)

from epics.ztc13_transparency_federation.transparency_registry import (
    TransparencyRegistry,
)

from epics.ztc13_transparency_federation.federated_transparency_registry import (
    FederatedTransparencyRegistry,
)


def test_finds_anchor_in_first_registry():

    registry_a = TransparencyRegistry()

    registry_a.add(
        TransparencyAnchor(
            attestation_id="att-001",
            anchor_id="anchor-001",
            transparency_root="root-001",
        )
    )

    federation = FederatedTransparencyRegistry(
        [registry_a]
    )

    assert federation.exists(
        "anchor-001"
    )


def test_finds_anchor_across_multiple_registries():

    registry_a = TransparencyRegistry()
    registry_b = TransparencyRegistry()

    registry_b.add(
        TransparencyAnchor(
            attestation_id="att-002",
            anchor_id="anchor-002",
            transparency_root="root-002",
        )
    )

    federation = FederatedTransparencyRegistry(
        [registry_a, registry_b]
    )

    assert federation.exists(
        "anchor-002"
    )


def test_returns_false_for_unknown_anchor():

    federation = FederatedTransparencyRegistry(
        []
    )

    assert not federation.exists(
        "missing-anchor"
    )
