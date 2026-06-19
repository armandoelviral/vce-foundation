from phase3.historical_replay_auditor.replay_audit_decision import (
    ReplayAuditDecision,
)

from phase3.replay_certification_engine.certificate_issuer import (
    CertificateIssuer,
)

from phase3.cryptographic_replay_report.report_builder import (
    ReportBuilder,
)

from phase3.cryptographic_replay_report.report_verifier import (
    ReportVerifier,
)

from phase3.cryptographic_replay_report.report_signature import (
    ReportSignature,
)

from phase3.cryptographic_replay_report.report_attestation import (
    ReportAttestation,
)

from phase3.cryptographic_replay_report.report_export import (
    ReportExport,
)


def test_end_to_end_cryptographic_replay_report():

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

    report = ReportBuilder.build(
        report_id="report-001",
        certificate=certificate,
    )

    assert (
        ReportVerifier.verify(
            report
        )
        is True
    )

    signature = ReportSignature(
        report_id="report-001",
        signature="sig-001",
    )

    assert (
        signature.signature
        == "sig-001"
    )

    attestation = (
        ReportAttestation.attest(
            attestation_id="att-001",
            report=report,
        )
    )

    assert (
        attestation.subject
        == "cryptographic_replay_report"
    )

    exported = ReportExport.export(
        report
    )

    assert (
        exported["report_id"]
        == "report-001"
    )

    assert (
        exported["certificate_id"]
        == "cert-001"
    )

    assert (
        exported["status"]
        == "PASS"
    )
