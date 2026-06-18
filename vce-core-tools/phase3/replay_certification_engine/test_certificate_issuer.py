from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.replay_certification_engine.certificate_issuer import (
    CertificateIssuer,
)


def test_issuer_creates_certificate():

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

    assert (
        certificate.certificate_id
        == "cert-001"
    )


def test_issuer_preserves_replay_id():

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

    assert (
        certificate.replay_id
        == "replay-001"
    )


def test_issuer_uses_decision_status():

    decision = ReplayAuditDecision(
        status="FAIL"
    )

    certificate = (
        CertificateIssuer.issue(
            certificate_id="cert-001",
            replay_id="replay-001",
            decision=decision,
        )
    )

    assert (
        certificate.status
        == "FAIL"
    )
