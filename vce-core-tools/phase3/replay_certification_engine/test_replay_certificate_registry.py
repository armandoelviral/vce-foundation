from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)


def test_registry_starts_empty():

    registry = ReplayCertificateRegistry()

    assert registry.count() == 0


def test_registry_accepts_certificate():

    registry = ReplayCertificateRegistry()

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry.add(
        certificate
    )

    assert registry.count() == 1


def test_registry_returns_certificate():

    registry = ReplayCertificateRegistry()

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry.add(
        certificate
    )

    recovered = registry.get(
        "cert-001"
    )

    assert recovered == certificate


def test_missing_certificate_returns_none():

    registry = ReplayCertificateRegistry()

    assert registry.get(
        "missing"
    ) is None
