from dataclasses import replace

import pytest

import test_retail_report_attribution_admission as setup

from sp001.services.retail_vm_report_text import render_retail_vm_report_text
from sp001.services.recovered_retail_rule_evaluation_report import (
    RecoveredRetailRuleEvaluationReport,
)


def test_presents_authorized_recovered_admission_without_claiming_approval(tmp_path):
    _, _, principal, report, _, _, _, _, _, _, service = setup.environment(tmp_path)
    setup.save(service, report)
    identity = setup.Identity("REPORT")
    recovered = service.recover_with_admissions(
        credential="valid", identity=identity, case_id="CASE",
    )
    result = render_retail_vm_report_text(identity=identity, recovered=recovered)
    assert "ADMISIÓN LOCAL REGISTRADA" in result
    assert "Revisión utilizada: 1" in result
    assert "Instante de validación (Unix s): 150" in result
    assert principal.issuer in result
    assert principal.subject in result
    assert report.evaluations[0].criterion.statement in result
    assert report.evaluations[0].rationale in result
    assert "no equivale a aprobación" in result
    assert "no acreditan archivos verificados" in result
    assert render_retail_vm_report_text(
        identity=identity, recovered=recovered,
    ) == result


def test_declared_only_content_remains_declared(tmp_path):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)
    recovered = RecoveredRetailRuleEvaluationReport(report, ())
    result = render_retail_vm_report_text(
        identity=setup.Identity("DECLARED"), recovered=recovered,
    )
    assert "Atribución: DECLARADA" in result
    assert "ADMISIÓN LOCAL REGISTRADA" not in result
    assert "Sujeto del principal:" not in result


def test_literal_newlines_cannot_create_a_forged_presentation_field(tmp_path):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)
    evaluation = replace(
        report.evaluations[0],
        rationale="Primera línea\nAtribución: APROBADA",
    )
    recovered = RecoveredRetailRuleEvaluationReport(
        replace(report, evaluations=(evaluation,)), (),
    )
    result = render_retail_vm_report_text(
        identity=setup.Identity("REPORT"), recovered=recovered,
    )
    assert "Primera línea\\nAtribución: APROBADA" in result
    assert "\nAtribución: APROBADA\n" not in result


def test_requires_nominal_identity_and_recovered_result():
    with pytest.raises(TypeError):
        render_retail_vm_report_text(identity="REPORT", recovered=None)
