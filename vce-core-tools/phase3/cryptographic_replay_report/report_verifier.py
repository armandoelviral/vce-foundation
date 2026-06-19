from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)


class ReportVerifier:

    @staticmethod
    def verify(
        report: CryptographicReplayReportRecord,
    ) -> bool:

        if not report.report_id:
            return False

        if not report.certificate_id:
            return False

        if not report.status:
            return False

        return True
