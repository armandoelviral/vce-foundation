from epics.ztc21_hardware_trust_anchors.hardware_trust_anchor import (
    HardwareTrustAnchor,
)

from epics.ztc21_hardware_trust_anchors.hardware_anchor_verifier import (
    HardwareAnchorVerifier,
)

from epics.ztc21_hardware_trust_anchors.hardware_trust_policy import (
    HardwareTrustPolicy,
)

from epics.ztc21_hardware_trust_anchors.hardware_admission_record import (
    HardwareAdmissionRecord,
)

from epics.ztc21_hardware_trust_anchors.trusted_hardware_registry import (
    TrustedHardwareRegistry,
)

from epics.ztc21_hardware_trust_anchors.hardware_trust_consensus import (
    HardwareTrustConsensus,
)


def test_end_to_end_hardware_trust_anchor_flow():

    aws_anchor = HardwareTrustAnchor(
        provider="aws",
        anchor_type="nitro_pcr",
        measurement_hash="hash-aws",
    )

    gcp_anchor = HardwareTrustAnchor(
        provider="gcp",
        anchor_type="sev_snp",
        measurement_hash="hash-gcp",
    )

    azure_anchor = HardwareTrustAnchor(
        provider="azure",
        anchor_type="azure_claim",
        measurement_hash="hash-azure",
    )

    assert HardwareAnchorVerifier.verify(
        aws_anchor
    )

    assert HardwareAnchorVerifier.verify(
        gcp_anchor
    )

    assert HardwareAnchorVerifier.verify(
        azure_anchor
    )

    policy = HardwareTrustPolicy()

    aws_admitted = policy.admit(
        verified=True,
    )

    gcp_admitted = policy.admit(
        verified=True,
    )

    azure_admitted = policy.admit(
        verified=True,
    )

    registry = TrustedHardwareRegistry()

    registry.add(
        HardwareAdmissionRecord(
            provider="aws",
            admitted=aws_admitted,
            reason="hardware_anchor_verified",
        )
    )

    registry.add(
        HardwareAdmissionRecord(
            provider="gcp",
            admitted=gcp_admitted,
            reason="hardware_anchor_verified",
        )
    )

    registry.add(
        HardwareAdmissionRecord(
            provider="azure",
            admitted=azure_admitted,
            reason="hardware_anchor_verified",
        )
    )

    assert registry.is_trusted(
        "aws"
    )

    assert registry.is_trusted(
        "gcp"
    )

    assert registry.is_trusted(
        "azure"
    )

    consensus = HardwareTrustConsensus()

    assert consensus.has_consensus(
        total_providers=3,
        trusted_providers=3,
    )
