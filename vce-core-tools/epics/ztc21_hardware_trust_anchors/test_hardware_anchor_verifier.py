from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)

from epics.ztc21_hardware_trust_anchors.hardware_anchor_verifier import (
    HardwareAnchorVerifier,
)


def test_accepts_supported_aws_anchor():

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    assert HardwareAnchorVerifier.verify(anchor)


def test_accepts_supported_gcp_anchor():

    anchor = HardwareTrustAnchor(
        provider="gcp",
        anchor_type="sev_snp",
        measurement_hash="hash-002",
    )

    assert HardwareAnchorVerifier.verify(anchor)


def test_rejects_unsupported_provider():

    anchor = HardwareTrustAnchor(
        provider="unknown",
        anchor_type="nitro_pcr",
        measurement_hash="hash-001",
    )

    assert not HardwareAnchorVerifier.verify(anchor)


def test_rejects_missing_measurement_hash():

    anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="",
    )

    assert not HardwareAnchorVerifier.verify(anchor)
