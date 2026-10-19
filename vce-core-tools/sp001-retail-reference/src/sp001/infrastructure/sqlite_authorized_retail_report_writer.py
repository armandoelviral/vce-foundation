import sqlite3
from collections.abc import Callable
from pathlib import Path

from sp001.contracts.case_access_context import ValidatedCaseAccessContext
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
    RetailRuleEvaluationReportIdentity,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report as serialize,
    deserialize_retail_rule_evaluation_report as deserialize,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_retail_rule_evaluation_reports import (
    SqliteRetailRuleEvaluationReportStore,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)
from sp001.services.retail_report_access_policy import (
    required_retail_report_permissions, token_allows_retail_report,
)
from sp001.services.retail_rule_evaluation_report import (
    RetailRuleEvaluationReport,
)


class SqliteAuthorizedRetailReportWriter:
    """Trusted writer capability; caller must supply authenticated context.

    Local grants and reports use one database and transaction.
    Does not authenticate credentials or establish evaluator attribution.
    """

    def __init__(
        self, *, database_path: str | Path,
        expected_audience: str, clock: Callable[[], int],
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError("database_path must be a string or Path")
        if not str(database_path).strip() or str(database_path) == ":memory:":
            raise ValueError("database_path must identify a file")
        if not isinstance(expected_audience, str):
            raise TypeError("expected_audience must be a string")
        if not expected_audience.strip():
            raise ValueError("expected_audience must not be empty")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._path = str(database_path)
        self._audience = expected_audience
        self._clock = clock
        # Public initializers establish both schemas in the same database.
        SqliteCaseAccessGrants(database_path=database_path)
        SqliteRetailRuleEvaluationReportStore(database_path=database_path)

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

    def _authorize(self, connection, access, case_id):
        now = self._clock()
        if type(now) is not int:
            raise TypeError("clock must return integer Unix seconds")
        if now < 0:
            raise ValueError("clock must return nonnegative Unix seconds")
        if (
            access.audience != self._audience
            or not access.issued_at <= access.not_before <= now < access.expires_at
        ):
            raise RetailReportAuthenticationRejected("access context unusable")
        if not token_allows_retail_report(
            access=access, case_id=case_id,
            expected_audience=self._audience,
            at_time=now, recover_only=False,
        ):
            raise RetailReportAccessDenied("report access denied")
        for permission in required_retail_report_permissions(
            case_id=case_id, recover_only=False,
        ):
            row = connection.execute(
                """
                SELECT 1 FROM case_access_grants
                WHERE issuer=? AND subject=? AND case_id=? AND operation=?
                  AND revoked=0 AND valid_from<=? AND expires_at>?
                LIMIT 1
                """,
                (
                    access.principal.issuer, access.principal.subject,
                    permission.case_id, permission.operation.value, now, now,
                ),
            ).fetchone()
            if row is None:
                raise RetailReportAccessDenied("report access denied")

    def save_authorized(self, *, access, identity, report):
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")

        document = serialize(report)
        validated = deserialize(document)
        if validated != report:
            raise ValueError("serialized report content differs")

        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._authorize(connection, access, report.case_id)
            existing = connection.execute(
                "SELECT document FROM retail_rule_evaluation_reports "
                "WHERE report_id=?",
                (identity.report_id,),
            ).fetchone()
            if existing is not None:
                if existing[0] != document:
                    raise RetailRuleEvaluationReportConflict(
                        "report identity is bound to a different document"
                    )
            else:
                connection.execute(
                    "INSERT INTO retail_rule_evaluation_reports "
                    "(report_id, document) VALUES (?, ?)",
                    (identity.report_id, document),
                )
            self._authorize(connection, access, report.case_id)
            connection.execute("COMMIT")
            return validated
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
