import sqlite3
from dataclasses import replace

import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.contracts.retail_rule_evaluation_report_store import (
    RetailRuleEvaluationReportConflict,
)
from sp001.infrastructure.sqlite_admitted_retail_report_writer import (
    SqliteAdmittedRetailReportWriter, RetailEvaluationAdmissionConflict,
)
from sp001.infrastructure.retail_rule_evaluation_admission_serialization import (
    deserialize_retail_rule_evaluation_admission,
)
from sp001.services.authenticated_retail_reports import RetailReportAccessDenied
from sp001.services.transactional_authenticated_retail_reports import (
    TransactionalAuthenticatedRetailReports,
)


def documents(path):
    with sqlite3.connect(path) as connection:
        reports = connection.execute(
            "SELECT report_id, document "
            "FROM retail_rule_evaluation_reports ORDER BY report_id"
        ).fetchall()
        admissions = connection.execute(
            "SELECT evaluation_id, document "
            "FROM retail_evaluation_admissions ORDER BY evaluation_id"
        ).fetchall()
    return reports, admissions


def lose_confirmation(path, backend, service, report, monkeypatch):
    failure = OSError("synthetic confirmation loss after successful commit")
    observed = []

    class ConfirmationLostConnection(sqlite3.Connection):
        def execute(self, sql, parameters=()):
            result = super().execute(sql, parameters)
            if sql.strip().upper() == "COMMIT":
                observed.append(not self.in_transaction)
                raise failure
            return result

    real_connect = sqlite3.connect

    def connect():
        connection = real_connect(
            path, timeout=5.0, isolation_level=None,
            factory=ConfirmationLostConnection,
        )
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    with monkeypatch.context() as patch:
        patch.setattr(backend, "_connect", connect)
        with pytest.raises(OSError) as caught:
            setup.save(service, report)
        assert caught.value is failure

    assert observed == [True]
    assert setup.counts(path) == (1, 1)
    return documents(path)


def reopen(path, auth):
    backend = SqliteAdmittedRetailReportWriter(
        database_path=path, expected_audience="REPORTS", clock=lambda: 150,
    )
    return TransactionalAuthenticatedRetailReports(
        authenticator=auth, backend=backend,
        expected_audience="REPORTS", clock=lambda: 150,
    )


def test_reopen_recover_and_retry_preserve_exact_confirmed_content(
    tmp_path, monkeypatch,
):
    (
        path, _, principal, report, _, _, _, _,
        auth, backend, service,
    ) = setup.environment(tmp_path)
    original = lose_confirmation(
        path, backend, service, report, monkeypatch,
    )
    restored = reopen(path, auth)

    before = auth.calls
    assert restored.recover(
        credential="valid", identity=setup.Identity("REPORT"), case_id="CASE",
    ) == report
    assert setup.save(restored, report, references=()) == report
    assert setup.save(restored, report) == report
    assert auth.calls == before + 3

    assert setup.counts(path) == (1, 1)
    assert documents(path) == original
    admission = deserialize_retail_rule_evaluation_admission(
        original[1][0][1],
    )
    assert admission.evaluation == report.evaluations[0]
    assert admission.principal == principal
    assert admission.binding_snapshot.binding.revision == 1
    assert admission.validated_at == 150


@pytest.mark.parametrize("report_id", ["REPORT", "OTHER-REPORT"])
def test_contradictory_content_cannot_replace_confirmed_result(
    tmp_path, monkeypatch, report_id,
):
    (
        path, _, _, report, _, _, _, _,
        auth, backend, service,
    ) = setup.environment(tmp_path)
    original = lose_confirmation(
        path, backend, service, report, monkeypatch,
    )
    restored = reopen(path, auth)
    changed = replace(report, evaluations=(
        replace(report.evaluations[0], rationale="Contradictory content."),
    ))
    expected = (
        RetailRuleEvaluationReportConflict
        if report_id == "REPORT"
        else RetailEvaluationAdmissionConflict
    )
    with pytest.raises(expected):
        setup.save(
            restored, changed, report_id=report_id, references=(),
        )
    assert setup.counts(path) == (1, 1)
    assert documents(path) == original


def test_revoked_permissions_block_recovery_and_retry_after_confirmation_loss(
    tmp_path, monkeypatch,
):
    (
        path, _, principal, report, _, _, grants, definitions,
        auth, backend, service,
    ) = setup.environment(tmp_path)
    original = lose_confirmation(
        path, backend, service, report, monkeypatch,
    )
    for index, grant in enumerate(definitions):
        assert grants.apply(record=GrantAdministrationRecord(
            f"LOSS-REVOKE-{index}", principal, Action.REVOKE, grant, 150,
        ))

    restored = reopen(path, auth)
    before = auth.calls
    with pytest.raises(RetailReportAccessDenied):
        restored.recover(
            credential="valid", identity=setup.Identity("REPORT"), case_id="CASE",
        )
    with pytest.raises(RetailReportAccessDenied):
        setup.save(restored, report, references=())
    assert auth.calls == before + 2

    # Authorization withdrawal does not undo the earlier confirmed transaction.
    assert setup.counts(path) == (1, 1)
    assert documents(path) == original
