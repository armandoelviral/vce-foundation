from phase3.replay_certification_engine.replay_certificate_record import (
    ReplayCertificateRecord,
)

from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)


class ReportBuilder:

    @staticmethod
    def build(
        report_id: str,
        certificate: ReplayCertificateRecord,
    ) -> CryptographicReplayReportRecord:

        return CryptographicReplayReportRecord(
            report_id=report_id,
            certificate_id=certificate.certificate_id,
            status=certificate.status,
        )
