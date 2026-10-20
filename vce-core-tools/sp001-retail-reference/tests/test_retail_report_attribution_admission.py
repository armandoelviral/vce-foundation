import sqlite3
from dataclasses import replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.case_access_context import (
    CaseAccessOperation as Operation, CaseAccessPermission,
    ValidatedCaseAccessContext,
)
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.retail_context_rule_observation import (
    RetailContextRuleObservation, RuleObservationStatus,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole
from sp001.contracts.retail_rule_criterion import RetailRuleCriterion
from sp001.contracts.retail_rule_evaluation_record import RetailRuleEvaluationRecord
from sp001.contracts.retail_evaluator_binding import (
    RetailEvaluatorBinding, RetailEvaluatorBindingSnapshot,
)
from sp001.contracts.retail_evaluator_binding_change import RetailEvaluatorBindingChange
from sp001.contracts.retail_evaluation_binding_reference import (
    RetailEvaluationBindingReference as Reference,
)
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportIdentity as Identity,
)
from sp001.infrastructure.sqlite_case_access_grants import SqliteCaseAccessGrants
from sp001.infrastructure.sqlite_retail_evaluator_bindings import (
    SqliteRetailEvaluatorBindings,
)
from sp001.infrastructure.sqlite_admitted_retail_report_writer import (
    SqliteAdmittedRetailReportWriter, RetailEvaluationAdmissionConflict,
)
from sp001.infrastructure.retail_rule_evaluation_admission_serialization import (
    deserialize_retail_rule_evaluation_admission,
)
from sp001.services.authenticated_retail_reports import RetailReportAccessDenied
from sp001.services.retail_evaluator_binding_validation import (
    RetailEvaluatorBindingRejected,
)
from sp001.services.retail_rule_evaluation_report import RetailRuleEvaluationReport
from sp001.services.transactional_authenticated_retail_reports import (
    TransactionalAuthenticatedRetailReports,
)


def environment(tmp_path):
    path = tmp_path / "shared.sqlite3"
    now = [150]
    principal = AuthenticatedPrincipal("ISSUER", "SUBJECT")
    actor = RetailProcessActor(
        "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
        RetailProcessRole("ROLE", "CUSTOMER", "VM reviewer"),
    )
    evaluation = RetailRuleEvaluationRecord(
        "EVAL",
        RetailContextRuleObservation(
            "OBS", "RULE", "SNAPSHOT", 1, "CASE",
            RuleObservationStatus.CONFORMANT, ("EVIDENCE",),
        ),
        RetailRuleCriterion("RULE", 1, "Synthetic criterion."),
        actor, datetime(2026, 1, 1, tzinfo=timezone.utc), "Declared rationale.",
    )
    report = RetailRuleEvaluationReport("CASE", (evaluation,), ())
    backend = SqliteAdmittedRetailReportWriter(
        database_path=path, expected_audience="REPORTS", clock=lambda: now[0],
    )
    grants = SqliteCaseAccessGrants(database_path=path)
    permissions = tuple(CaseAccessPermission("CASE", op) for op in (
        Operation.SAVE_RETAIL_REPORT, Operation.READ_RETAIL_REPORT,
    ))
    definitions = []
    for index, permission in enumerate(permissions):
        grant = CaseAccessGrant(
            f"G-{index}", principal, permission, 100, 300,
        )
        grants.apply(record=GrantAdministrationRecord(
            f"GE-{index}", principal, Action.GRANT, grant, 100,
        ))
        definitions.append(grant)
    binding = RetailEvaluatorBinding(
        "BINDING", 1, principal, actor, "CASE", 100, 200,
    )
    bindings = SqliteRetailEvaluatorBindings(database_path=path)
    bindings.apply(change=RetailEvaluatorBindingChange(
        "BE-1", RetailEvaluatorBindingSnapshot(binding, False), principal, 100,
    ))

    class Authenticator:
        calls = 0
        def authenticate(self, *, credential):
            self.calls += 1
            return ValidatedCaseAccessContext(
                principal, "REPORTS", 100, 100, 300, permissions,
            ) if credential == "valid" else None

    auth = Authenticator()
    service = TransactionalAuthenticatedRetailReports(
        authenticator=auth, backend=backend,
        expected_audience="REPORTS", clock=lambda: now[0],
    )
    return path, now, principal, report, binding, bindings, grants, definitions, auth, backend, service


def counts(path):
    with sqlite3.connect(path) as connection:
        return tuple(connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0] for table in (
            "retail_rule_evaluation_reports", "retail_evaluation_admissions",
        ))


def save(service, report, report_id="REPORT", references=None):
    return service.save_with_admissions(
        credential="valid", identity=Identity(report_id), report=report,
        binding_references=(
            (Reference("EVAL", "BINDING", 1),)
            if references is None else references
        ),
    )


def test_admits_once_reopens_and_preserves_original_receipt(tmp_path):
    path, _, _, report, _, _, _, _, auth, _, service = environment(tmp_path)
    assert save(service, report) == report
    assert save(service, report, references=()) == report
    assert auth.calls == 2
    assert counts(path) == (1, 1)
    with sqlite3.connect(path) as connection:
        encoded = connection.execute(
            "SELECT document FROM retail_evaluation_admissions"
        ).fetchone()[0]
    admission = deserialize_retail_rule_evaluation_admission(encoded)
    assert admission.evaluation == report.evaluations[0]
    assert admission.binding_snapshot.binding.revision == 1
    assert admission.validated_at == 150
    assert service.recover(
        credential="valid", identity=Identity("REPORT"), case_id="CASE",
    ) == report


def test_revocation_preserves_reuse_but_blocks_new_evaluation(tmp_path):
    path, _, principal, report, binding, bindings, _, _, _, _, service = environment(tmp_path)
    save(service, report)
    bindings.apply(change=RetailEvaluatorBindingChange(
        "BE-2",
        RetailEvaluatorBindingSnapshot(replace(binding, revision=2), True),
        principal, 150,
    ))
    assert save(service, report, "SECOND", references=()) == report
    changed = replace(report, evaluations=(
        replace(report.evaluations[0], evaluation_id="NEW"),
    ))
    with pytest.raises(RetailEvaluatorBindingRejected):
        save(service, changed, "THIRD", (Reference("NEW", "BINDING", 2),))
    assert counts(path) == (2, 1)


def test_same_evaluation_identity_different_content_is_conflict(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = environment(tmp_path)
    save(service, report)
    changed = replace(report, evaluations=(
        replace(report.evaluations[0], rationale="Different content."),
    ))
    with pytest.raises(RetailEvaluationAdmissionConflict):
        save(service, changed, "SECOND", references=())
    assert counts(path) == (1, 1)


def test_batch_failure_rolls_back_earlier_admission_and_report(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = environment(tmp_path)
    second = replace(report.evaluations[0], evaluation_id="SECOND")
    batch = replace(report, evaluations=(*report.evaluations, second))
    with pytest.raises(RetailReportAccessDenied):
        save(service, batch)
    assert counts(path) == (0, 0)


def test_old_report_is_not_promoted_by_identical_retry(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = environment(tmp_path)
    service.save(credential="valid", identity=Identity("REPORT"), report=report)
    with pytest.raises(RetailReportAccessDenied, match="no recorded admission"):
        save(service, report)
    assert counts(path) == (1, 0)
    assert service.recover(
        credential="valid", identity=Identity("REPORT"), case_id="CASE",
    ) == report


def test_revoked_grant_blocks_admitted_retry(tmp_path):
    path, _, principal, report, _, _, grants, definitions, auth, _, service = environment(tmp_path)
    save(service, report)
    for index, grant in enumerate(definitions):
        grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{index}", principal, Action.REVOKE, grant, 150,
        ))
    with pytest.raises(RetailReportAccessDenied):
        save(service, report, references=())
    assert auth.calls == 2
    assert counts(path) == (1, 1)


def test_binding_expiration_before_commit_rolls_back_everything(tmp_path, monkeypatch):
    path, now, _, report, _, _, _, _, _, backend, service = environment(tmp_path)
    original = backend._validate_reference
    calls = []

    def validate(*args):
        result = original(*args)
        calls.append(True)
        if len(calls) == 1:
            now[0] = 200
        return result

    monkeypatch.setattr(backend, "_validate_reference", validate)
    with pytest.raises(RetailEvaluatorBindingRejected):
        save(service, report)
    assert counts(path) == (0, 0)


def test_stale_expected_revision_does_not_persist(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = environment(tmp_path)
    with pytest.raises(RetailEvaluatorBindingRejected, match="revision_conflict"):
        save(service, report, references=(Reference("EVAL", "BINDING", 2),))
    assert counts(path) == (0, 0)
