import sqlite3
from dataclasses import replace

import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action, GrantAdministrationRecord,
)
from sp001.contracts.retail_evaluator_binding import RetailEvaluatorBindingSnapshot
from sp001.contracts.retail_evaluator_binding_change import RetailEvaluatorBindingChange
from sp001.infrastructure.sqlite_admitted_retail_report_writer import (
    RetailEvaluationAdmissionConflict,
)
from sp001.services.authenticated_retail_reports import (
    RetailReportAccessDenied, RetailReportAuthenticationRejected,
)


def recover(service, identity="REPORT", case_id="CASE", credential="valid"):
    return service.recover_with_admissions(
        credential=credential, identity=setup.Identity(identity), case_id=case_id,
    )


def test_returns_recorded_principal_binding_and_revision(tmp_path):
    path, _, principal, report, _, _, _, _, auth, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    before = auth.calls
    result = recover(service)
    assert auth.calls == before + 1
    assert result.report == report
    assert result.declared_only_evaluation_ids == ()
    assert len(result.admissions) == 1
    admission = result.admissions[0]
    assert admission.principal == principal
    assert admission.evaluation == report.evaluations[0]
    assert admission.binding_snapshot.binding.revision == 1
    assert admission.validated_at == 150
    assert setup.counts(path) == (1, 1)


def test_legacy_report_keeps_explicitly_declared_attribution(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    service.save(credential="valid", identity=setup.Identity("REPORT"), report=report)
    result = recover(service)
    assert result.report == report
    assert result.admissions == ()
    assert result.declared_only_evaluation_ids == ("EVAL",)
    assert setup.counts(path) == (1, 0)


def test_mixed_report_does_not_infer_admission_for_unknown_evaluation(tmp_path):
    _, _, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    second = replace(report.evaluations[0], evaluation_id="DECLARED")
    mixed = replace(report, evaluations=(*report.evaluations, second))
    service.save(credential="valid", identity=setup.Identity("MIXED"), report=mixed)
    result = recover(service, "MIXED")
    assert result.report == mixed
    assert tuple(a.evaluation.evaluation_id for a in result.admissions) == ("EVAL",)
    assert result.declared_only_evaluation_ids == ("DECLARED",)


def test_binding_revocation_preserves_historical_admission(tmp_path):
    _, _, principal, report, binding, bindings, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    original = recover(service)
    bindings.apply(change=RetailEvaluatorBindingChange(
        "REVOKED", RetailEvaluatorBindingSnapshot(
            replace(binding, revision=2), True,
        ), principal, 150,
    ))
    assert recover(service) == original
    assert original.admissions[0].binding_snapshot.binding.revision == 1
    assert not original.admissions[0].binding_snapshot.revoked


def test_revoked_case_grants_deny_existing_and_missing_report(tmp_path):
    _, _, principal, report, _, _, grants, definitions, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    for index, grant in enumerate(definitions):
        grants.apply(record=GrantAdministrationRecord(
            f"REVOKE-{index}", principal, Action.REVOKE, grant, 150,
        ))
    for identity in ("REPORT", "MISSING"):
        with pytest.raises(RetailReportAccessDenied):
            recover(service, identity)


def test_missing_report_and_invalid_credential_remain_distinct(tmp_path):
    _, _, _, _, _, _, _, _, _, _, service = setup.environment(tmp_path)
    assert recover(service, "MISSING") is None
    with pytest.raises(RetailReportAuthenticationRejected):
        recover(service, credential="invalid")


def test_conflicting_persisted_admission_is_not_returned(tmp_path):
    path, _, _, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    # Keep the admission structurally valid while making its evaluation differ.
    import json
    with sqlite3.connect(path) as connection:
        document = connection.execute(
            "SELECT document FROM retail_evaluation_admissions WHERE evaluation_id='EVAL'"
        ).fetchone()[0]
        envelope = json.loads(document)
        nested = json.loads(envelope["admission"]["evaluation_document"])
        evaluation = nested["report"]["fields"]["evaluations"]["items"][0]
        evaluation["fields"]["rationale"] = "Altered evaluation."
        envelope["admission"]["evaluation_document"] = json.dumps(
            nested, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        )
        changed = json.dumps(
            envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        )
        connection.execute(
            "UPDATE retail_evaluation_admissions SET document=? WHERE evaluation_id='EVAL'",
            (changed,),
        )
    with pytest.raises(RetailEvaluationAdmissionConflict):
        recover(service)


def test_expiration_before_return_rejects_entire_result(tmp_path, monkeypatch):
    _, now, _, report, _, _, _, _, _, backend, service = setup.environment(tmp_path)
    setup.save(service, report)
    original = backend._authorize
    calls = []

    def authorize(*args, **kwargs):
        if calls:
            now[0] = 300
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(backend, "_authorize", authorize)
    with pytest.raises(RetailReportAuthenticationRejected):
        recover(service)
