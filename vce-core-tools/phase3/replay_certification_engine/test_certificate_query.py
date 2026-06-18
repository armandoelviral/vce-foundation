from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)

from phase3.replay_certification_engine.certificate_query import (
    CertificateQuery,
)


def test_query_returns_certificate():

    registry = ReplayCertificateRegistry()

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry.add(
        certificate
    )

    query = CertificateQuery(
        registry
    )

    result = query.by_id(
        "cert-001"
    )

    assert result == certificate


def test_query_returns_none_for_missing():

    registry = ReplayCertificateRegistry()

    query = CertificateQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    registry = ReplayCertificateRegistry()

    certificate = ReplayCertificateRecord(
        certificate_id="cert-001",
        replay_id="replay-001",
        status="PASS",
    )

    registry.add(
        certificate
    )

    query = CertificateQuery(
        registry
    )

    result = query.by_id(
        "cert-001"
    )

    assert result.status == "PASS"
