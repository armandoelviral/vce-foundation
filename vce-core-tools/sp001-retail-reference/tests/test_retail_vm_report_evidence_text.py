from dataclasses import replace

import pytest

import test_retail_report_attribution_admission as setup

from sp001.contracts.evidence_file_expectation import EvidenceFileExpectation
from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity
from sp001.infrastructure.evidence_file_comparison import compare_evidence_file
from sp001.services.knowledge_source_integrity import digest_knowledge_source_content
from sp001.services.recovered_retail_rule_evaluation_report import (
    RecoveredRetailRuleEvaluationReport,
)
from sp001.services.retail_report_evidence_comparison import (
    bind_retail_report_evidence_comparisons,
)
from sp001.services.retail_vm_report_evidence_text import (
    render_retail_vm_report_evidence_text as render,
)
from sp001.services.retail_vm_report_text import render_retail_vm_report_text


def expected():
    return EvidenceFileExpectation(
        KnowledgeSourceIdentity(
            "EVIDENCE", "1",
            digest_knowledge_source_content(content=b"original"),
        ),
        8,
    )


@pytest.mark.parametrize("scenario,label", [
    ("match", "COINCIDENCIA DE BYTES"),
    ("different", "CONTENIDO DIFERENTE"),
    ("missing", "ARCHIVO NO ENCONTRADO"),
    ("limit", "LÍMITE DE LECTURA EXCEDIDO"),
    ("unchecked", "SIN COMPROBAR"),
    ("undeclared", "SIN EXPECTATIVA DECLARADA"),
])
def test_presents_evidence_without_changing_original_report(
    tmp_path, scenario, label,
):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)
    recovered = RecoveredRetailRuleEvaluationReport(report, ())
    expectation = expected()
    path = tmp_path / "evidence.bin"
    comparisons = ()
    expectations = (expectation,)
    if scenario == "undeclared":
        expectations = ()
    elif scenario != "unchecked":
        if scenario == "match":
            path.write_bytes(b"original")
        elif scenario == "different":
            path.write_bytes(b"modified")
        elif scenario == "limit":
            path.write_bytes(b"x" * 9)
        comparisons = (compare_evidence_file(
            expectation=expectation, path=path, max_bytes=8,
        ),)
    evidence = bind_retail_report_evidence_comparisons(
        report=report, expectations=expectations, comparisons=comparisons,
    )
    original_text = render_retail_vm_report_text(
        identity=setup.Identity("REPORT"), recovered=recovered,
    )
    output = render(
        identity=setup.Identity("REPORT"), recovered=recovered,
        evidence=evidence,
    )
    assert output.startswith(original_text)
    assert label in output
    assert "no acredita autenticidad" in output
    assert recovered.report is report
    assert evidence.report is report
    assert report.evaluations[0].observation.status.value == "CONFORMANT"
    if scenario == "match":
        assert expectation.identity.source_content_digest.value in output
        assert "Tamaño observado (bytes): 8" in output
    if scenario in ("unchecked", "undeclared", "missing", "limit"):
        assert "SHA-256 observado:" not in output


def test_rejects_comparisons_for_different_report(tmp_path):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)
    changed = replace(report, evaluations=(
        replace(report.evaluations[0], rationale="Different evaluation."),
    ))
    evidence = bind_retail_report_evidence_comparisons(
        report=changed, expectations=(), comparisons=(),
    )
    with pytest.raises(ValueError, match="different report"):
        render(
            identity=setup.Identity("REPORT"),
            recovered=RecoveredRetailRuleEvaluationReport(report, ()),
            evidence=evidence,
        )


def test_rejects_incomplete_reference_container(tmp_path):
    _, _, _, report, _, _, _, _, _, _, _ = setup.environment(tmp_path)
    evidence = bind_retail_report_evidence_comparisons(
        report=report, expectations=(), comparisons=(),
    )
    with pytest.raises(ValueError, match="incomplete"):
        render(
            identity=setup.Identity("REPORT"),
            recovered=RecoveredRetailRuleEvaluationReport(report, ()),
            evidence=replace(evidence, references=()),
        )
