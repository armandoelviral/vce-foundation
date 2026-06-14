from epics.ztc13_transparency_federation.transparency_anchor import (
    TransparencyAnchor,
)
from epics.ztc13_transparency_federation.transparency_registry import (
    TransparencyRegistry,
)


def test_registry_stores_anchor():

    registry = TransparencyRegistry()

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    registry.add(anchor)

    assert registry.exists("anchor-001")


def test_registry_returns_anchor():

    registry = TransparencyRegistry()

    anchor = TransparencyAnchor(
        attestation_id="att-001",
        anchor_id="anchor-001",
        transparency_root="root-001",
    )

    registry.add(anchor)

    stored = registry.get("anchor-001")

    assert stored.anchor_id == "anchor-001"


def test_registry_returns_none_for_unknown_anchor():

    registry = TransparencyRegistry()

    assert registry.get("missing") is None
