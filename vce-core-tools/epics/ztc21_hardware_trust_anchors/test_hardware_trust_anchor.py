from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)


def test_anchor_contains_provider():

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    assert anchor.provider == "aws"


def test_anchor_contains_type_and_measurement():

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    assert anchor.anchor_type == "nitro_pcr"
    assert anchor.measurement_hash == "hash-001"


def test_anchor_serializes():

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    assert anchor.to_dict() == {
        "provider": "aws",
        "anchor_type": "nitro_pcr",
        "measurement_hash": "hash-001",
    }
