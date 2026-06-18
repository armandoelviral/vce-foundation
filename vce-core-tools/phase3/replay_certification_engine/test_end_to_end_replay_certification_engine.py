from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.replay_certification_engine.certificate_issuer import (
    CertificateIssuer,
)

from phase3.replay_certification_engine.replay_certificate_registry import (
    ReplayCertificateRegistry,
)

from phase3.replay_certification_engine.certificate_verifier import (
    CertificateVerifier,
)

from phase3.replay_certification_engine.certificate_query import (
    CertificateQuery,
)

from phase3.replay_certification_engine.certificate_report import (
    CertificateReport,
)

from phase3.replay_certification_engine.certificate_attestation import (
    CertificateAttestation,
)


def test_end_to_end_replay_certification_engine():

    decision = ReplayAuditDecision(
        status="PASS"
    )

    certificate = (
        CertificateIssuer.issue(
            certificate_id="cert-001",
            replay_id="replay-001",
            decision=decision,
        )
    )

    registry = ReplayCertificateRegistry()

    registry.add(
        certificate
    )

    assert (
        CertificateVerifier.verify(
            certificate
        )
        is True
    )

    query = CertificateQuery(
        registry
    )

    recovered = query.by_id(
        "cert-001"
    )

    assert recovered == certificate

    report = CertificateReport(
        registry
    )

    assert (
        report.certificate_count()
        == 1
    )

    assert (
        report.certificate_ids()
        == ["cert-001"]
    )

    attestation = (
        CertificateAttestation.attest(
            attestation_id="att-001",
            certificate=certificate,
        )
    )

    assert (
        attestation.subject
        == "replay_certificate"
    )

    assert (
        attestation.evidence_hash
        == "cert-001"
    )
