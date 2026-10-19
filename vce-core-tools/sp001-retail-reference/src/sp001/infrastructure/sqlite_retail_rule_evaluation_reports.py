import sqlite3
from pathlib import Path

from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
    RetailRuleEvaluationReportIdentity,
    StoredRetailRuleEvaluationReport,
)


class SqliteRetailRuleEvaluationReportStore:
    """Append-only document adapter; no authorization or authenticity claims."""

    def __init__(self, *, database_path: str | Path) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or Path")
        if not str(database_path).strip() or str(database_path) == ":memory:":
            raise ValueError("database_path must identify a file")
        self._path = str(database_path)
        connection = self._connect()
        try:
            mode = connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if mode.lower() != "wal":
                raise RuntimeError("WAL mode was not established")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS retail_rule_evaluation_reports (
                    report_id TEXT PRIMARY KEY NOT NULL,
                    document TEXT NOT NULL
                )
                """
            )
        finally:
            connection.close()

    def _connect(self):
        connection = sqlite3.connect(
            self._path, timeout=5.0, isolation_level=None,
        )
        try:
            connection.execute("PRAGMA synchronous=FULL")
        except BaseException:
            connection.close()
            raise
        return connection

    def put(
        self, *, report: StoredRetailRuleEvaluationReport
    ) -> StoredRetailRuleEvaluationReport:
        if not isinstance(report, StoredRetailRuleEvaluationReport):
            raise TypeError("report must be a StoredRetailRuleEvaluationReport")

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                INSERT INTO retail_rule_evaluation_reports (report_id, document)
                VALUES (?, ?)
                ON CONFLICT(report_id) DO NOTHING
                """,
                (report.identity.report_id, report.document),
            )
            row = connection.execute(
                """
                SELECT document FROM retail_rule_evaluation_reports
                WHERE report_id = ?
                """,
                (report.identity.report_id,),
            ).fetchone()
            if row is None:
                raise RuntimeError("inserted or existing report was not found")
            if row[0] != report.document:
                raise RetailRuleEvaluationReportConflict(
                    "report identity is bound to a different document"
                )
            stored = StoredRetailRuleEvaluationReport(
                identity=report.identity, document=row[0],
            )
            connection.execute("COMMIT")
            return stored
        except BaseException as error:
            if connection.in_transaction:
                try:
                    connection.execute("ROLLBACK")
                except BaseException as rollback_error:
                    error.add_note(
                        "Rollback also failed: "
                        + type(rollback_error).__name__
                    )
            raise
        finally:
            connection.close()

    def get(
        self, *, identity: RetailRuleEvaluationReportIdentity
    ) -> StoredRetailRuleEvaluationReport | None:
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError(
                "identity must be a RetailRuleEvaluationReportIdentity"
            )
        connection = self._connect()
        try:
            row = connection.execute(
                """
                SELECT document FROM retail_rule_evaluation_reports
                WHERE report_id = ?
                """,
                (identity.report_id,),
            ).fetchone()
            if row is None:
                return None
            return StoredRetailRuleEvaluationReport(
                identity=identity, document=row[0],
            )
        finally:
            connection.close()
