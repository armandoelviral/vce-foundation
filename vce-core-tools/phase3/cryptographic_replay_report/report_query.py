class ReportQuery:

    def __init__(
        self,
        reports,
    ):

        self.reports = reports

    def by_id(
        self,
        report_id: str,
    ):

        return self.reports.get(
            report_id
        )
