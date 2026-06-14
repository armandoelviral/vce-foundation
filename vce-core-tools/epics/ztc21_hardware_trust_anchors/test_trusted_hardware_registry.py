from epics.ztc21_hardware_trust_anchors.hardware_admission_record import (
    HardwareAdmissionRecord,
)

from epics.ztc21_hardware_trust_anchors.trusted_hardware_registry import (
    TrustedHardwareRegistry,
)


def test_registry_stores_admitted_provider():

    registry = TrustedHardwareRegistry()

    record = HardwareAdmissionRecord(
        provider="aws",
        admitted=True,
        reason="hardware_anchor_verified",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_reports_trusted_provider():

    registry = TrustedHardwareRegistry()

    registry.add(
        HardwareAdmissionRecord(
            provider="aws",
            admitted=True,
            reason="hardware_anchor_verified",
        )
    )

    assert registry.is_trusted(
        "aws"
    )


def test_registry_returns_false_for_unknown_provider():

    registry = TrustedHardwareRegistry()

    assert not registry.is_trusted(
        "unknown"
    )


def test_registry_ignores_rejected_provider():

    registry = TrustedHardwareRegistry()

    registry.add(
        HardwareAdmissionRecord(
            provider="aws",
            admitted=False,
            reason="verification_failed",
        )
    )

    assert not registry.is_trusted(
        "aws"
    )
