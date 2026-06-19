from phase3.cryptographic_replay_report.cryptographic_replay_report_record import (
    CryptographicReplayReportRecord,
)


class ReportExport:

    @staticmethod
    def export(
        report: CryptographicReplayReportRecord,
    ):

        return report.to_dict()
