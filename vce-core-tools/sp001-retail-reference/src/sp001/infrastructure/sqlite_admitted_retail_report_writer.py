from sp001.services.recovered_retail_rule_evaluation_report import (
    RecoveredRetailRuleEvaluationReport,
)
from sp001.contracts.case_access_context import ValidatedCaseAccessContext
from sp001.contracts.retail_evaluation_binding_reference import (
    RetailEvaluationBindingReference,
)
from sp001.contracts.retail_rule_evaluation_admission import (
    RetailRuleEvaluationAdmission,
)
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity, RetailRuleEvaluationReportConflict,
)
from sp001.infrastructure.sqlite_authorized_retail_report_writer import (
    SqliteAuthorizedRetailReportWriter,
)
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report as serialize_report,
    deserialize_retail_rule_evaluation_report as deserialize_report,
)
from sp001.infrastructure.retail_rule_evaluation_admission_serialization import (
    serialize_retail_rule_evaluation_admission as serialize_admission,
    deserialize_retail_rule_evaluation_admission as deserialize_admission,
)
from sp001.services.authenticated_retail_reports import RetailReportAccessDenied
from sp001.services.retail_evaluator_binding_validation import (
    validate_retail_evaluator_binding,
)
from sp001.services.retail_rule_evaluation_report import RetailRuleEvaluationReport


def _evaluation_document(evaluation):
    return serialize_report(RetailRuleEvaluationReport(
        case_id=evaluation.observation.case_id,
        evaluations=(evaluation,), relations=(),
    ))


class RetailEvaluationAdmissionConflict(ValueError):
    """An evaluation identity or admission reference conflicts."""


class SqliteAdmittedRetailReportWriter(SqliteAuthorizedRetailReportWriter):
    """Adds explicit attribution admission; inherited saves remain declarative."""

    def __init__(self, *, database_path, expected_audience, clock):
        super().__init__(
            database_path=database_path,
            expected_audience=expected_audience, clock=clock,
        )
        self._bindings = SqliteRetailEvaluatorBindings(
            database_path=database_path,
        )
        connection = self._connect()
        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS retail_evaluation_admissions (
                    evaluation_id TEXT PRIMARY KEY NOT NULL,
                    document TEXT NOT NULL
                )
            """)
        finally:
            connection.close()

    def _validate_reference(self, connection, access, evaluation, reference):
        snapshot = self._bindings.read_snapshot_in_transaction(
            connection=connection, binding_id=reference.binding_id,
        )
        now = self._clock()
        validate_retail_evaluator_binding(
            snapshot=snapshot, principal=access.principal,
            actor=evaluation.evaluator, case_id=evaluation.observation.case_id,
            expected_binding_id=reference.binding_id,
            expected_revision=reference.expected_revision,
            at_time=now,
        )
        return snapshot, now

    def save_with_admissions_authorized(
        self, *, access, identity, report, binding_references,
    ):
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if type(report) is not RetailRuleEvaluationReport:
            raise TypeError("report must be a RetailRuleEvaluationReport")
        if type(binding_references) is not tuple:
            raise TypeError("binding_references must be a tuple")
        if any(type(ref) is not RetailEvaluationBindingReference
               for ref in binding_references):
            raise TypeError("invalid binding reference")
        references = {ref.evaluation_id: ref for ref in binding_references}
        if len(references) != len(binding_references):
            raise ValueError("duplicate evaluation reference")
        identities = {item.evaluation_id for item in report.evaluations}
        if not set(references) <= identities:
            raise ValueError("reference is outside the report")

        document = serialize_report(report)
        validated = deserialize_report(document)
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._authorize(connection, access, report.case_id)
            existing_report = connection.execute(
                "SELECT document FROM retail_rule_evaluation_reports "
                "WHERE report_id=?", (identity.report_id,),
            ).fetchone()
            if existing_report is not None and existing_report[0] != document:
                raise RetailRuleEvaluationReportConflict(
                    "report identity is bound to a different document"
                )

            pending = []
            for evaluation in validated.evaluations:
                row = connection.execute(
                    "SELECT document FROM retail_evaluation_admissions "
                    "WHERE evaluation_id=?", (evaluation.evaluation_id,),
                ).fetchone()
                reference = references.get(evaluation.evaluation_id)
                if row is not None:
                    admitted = deserialize_admission(row[0])
                    if (
                        admitted.evaluation.evaluation_id != evaluation.evaluation_id
                        or _evaluation_document(admitted.evaluation)
                        != _evaluation_document(evaluation)
                    ):
                        raise RetailEvaluationAdmissionConflict(
                            "evaluation identity is bound to different content"
                        )
                    if reference is not None and (
                        reference.binding_id
                        != admitted.binding_snapshot.binding.binding_id
                        or reference.expected_revision
                        != admitted.binding_snapshot.binding.revision
                    ):
                        raise RetailEvaluationAdmissionConflict(
                            "reference differs from original admission"
                        )
                    continue

                # Identical retries cannot promote a pre-existing report.
                if existing_report is not None:
                    raise RetailReportAccessDenied(
                        "existing report has no recorded admission"
                    )
                if reference is None:
                    raise RetailReportAccessDenied(
                        "new evaluation requires a binding reference"
                    )
                snapshot, now = self._validate_reference(
                    connection, access, evaluation, reference,
                )
                admission = RetailRuleEvaluationAdmission(
                    evaluation=evaluation, principal=access.principal,
                    binding_snapshot=snapshot, validated_at=now,
                )
                encoded = serialize_admission(admission)
                if deserialize_admission(encoded) != admission:
                    raise ValueError("admission serialization differs")
                connection.execute(
                    "INSERT INTO retail_evaluation_admissions "
                    "(evaluation_id, document) VALUES (?, ?)",
                    (evaluation.evaluation_id, encoded),
                )
                pending.append((evaluation, reference))

            if existing_report is None:
                connection.execute(
                    "INSERT INTO retail_rule_evaluation_reports "
                    "(report_id, document) VALUES (?, ?)",
                    (identity.report_id, document),
                )

            # Recheck time-sensitive conditions after all work, before commit.
            for evaluation, reference in pending:
                self._validate_reference(
                    connection, access, evaluation, reference,
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
                        "Rollback also failed: " + type(rollback_error).__name__
                    )
            raise
        finally:
            connection.close()

    def recover_with_admissions_authorized(
        self, *, access, identity, case_id,
    ):
        """Read grants, report and admissions in one SQLite snapshot."""
        if not isinstance(access, ValidatedCaseAccessContext):
            raise TypeError("access must be a ValidatedCaseAccessContext")
        if not isinstance(identity, RetailRuleEvaluationReportIdentity):
            raise TypeError("identity must be a report identity")
        if not isinstance(case_id, str):
            raise TypeError("case_id must be a string")
        if not case_id.strip():
            raise ValueError("case_id must not be empty")
        connection = self._connect()
        try:
            connection.execute("BEGIN")
            self._authorize(connection, access, case_id, recover_only=True)
            row = connection.execute(
                "SELECT document FROM retail_rule_evaluation_reports "
                "WHERE report_id=?", (identity.report_id,),
            ).fetchone()
            result = None
            if row is not None:
                report = deserialize_report(row[0])
                if report.case_id != case_id:
                    raise RetailReportAccessDenied("report access denied")
                admissions = []
                for evaluation in report.evaluations:
                    stored = connection.execute(
                        "SELECT document FROM retail_evaluation_admissions "
                        "WHERE evaluation_id=?", (evaluation.evaluation_id,),
                    ).fetchone()
                    if stored is None:
                        continue
                    admission = deserialize_admission(stored[0])
                    if _evaluation_document(admission.evaluation) != (
                        _evaluation_document(evaluation)
                    ):
                        raise RetailEvaluationAdmissionConflict(
                            "stored admission differs from report evaluation"
                        )
                    admissions.append(admission)
                result = RecoveredRetailRuleEvaluationReport(
                    report=report, admissions=tuple(admissions),
                )
            self._authorize(connection, access, case_id, recover_only=True)
            connection.execute("COMMIT")
            return result
        except BaseException as error:
            if connection.in_transaction:
                try:
                    connection.execute("ROLLBACK")
                except BaseException as rollback_error:
                    error.add_note(
                        "Rollback also failed: " + type(rollback_error).__name__
                    )
            raise
        finally:
            connection.close()
