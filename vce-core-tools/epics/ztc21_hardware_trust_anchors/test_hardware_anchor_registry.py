from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)

from epics.ztc21_hardware_trust_anchors.hardware_anchor_registry import (
    HardwareAnchorRegistry,
)


def test_registry_stores_anchor():

    registry = HardwareAnchorRegistry()

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    registry.add(anchor)

    assert registry.count() == 1


def test_registry_returns_anchor():

    registry = HardwareAnchorRegistry()

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    registry.add(anchor)

    anchors = registry.all()

    assert len(anchors) == 1
    assert anchors[0].provider == "aws"


def test_registry_starts_empty():

    registry = HardwareAnchorRegistry()

    assert registry.count() == 0


def test_registry_supports_multiple_providers():

    registry = HardwareAnchorRegistry()

    registry.add(
        HardwareTrustAnchor(
            provider="aws",
            anchor_type="nitro_pcr",
            measurement_hash="hash-001",
        )
    )

    registry.add(
        HardwareTrustAnchor(
            provider="gcp",
            anchor_type="sev_snp",
            measurement_hash="hash-002",
        )
    )

    registry.add(
        HardwareTrustAnchor(
            provider="azure",
            anchor_type="azure_claim",
            measurement_hash="hash-003",
        )
    )

    assert registry.count() == 3
