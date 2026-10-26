from sp001.infrastructure.evidence_file_comparison import (
    EvidenceFileComparisonStatus as FileStatus,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    serialize_retail_rule_evaluation_report,
)
from sp001.services.recovered_retail_rule_evaluation_report import (
    RecoveredRetailRuleEvaluationReport,
)
from sp001.services.retail_report_evidence_comparison import (
    RetailReportEvidenceComparison,
    UncheckedEvidenceStatus,
    bind_retail_report_evidence_comparisons,
)
from sp001.services.retail_vm_report_text import (
    render_retail_vm_report_text, _text,
)


_LABELS = {
    FileStatus.MATCH: "COINCIDENCIA DE BYTES",
    FileStatus.DIFFERENT: "CONTENIDO DIFERENTE",
    FileStatus.NOT_FOUND: "ARCHIVO NO ENCONTRADO",
    FileStatus.LIMIT_EXCEEDED: "SIN COMPARACIÓN: LÍMITE DE LECTURA EXCEDIDO",
    FileStatus.CHANGED_DURING_READ: "SIN CONCLUSIÓN: CAMBIO DURANTE LA LECTURA",
    UncheckedEvidenceStatus.EXPECTATION_MISSING: "SIN EXPECTATIVA DECLARADA",
    UncheckedEvidenceStatus.NOT_CHECKED: "SIN COMPROBAR",
}


def render_retail_vm_report_evidence_text(
    *, identity, recovered: RecoveredRetailRuleEvaluationReport,
    evidence: RetailReportEvidenceComparison,
) -> str:
    """Present supplied byte comparisons without changing evaluation outcomes."""
    if type(recovered) is not RecoveredRetailRuleEvaluationReport:
        raise TypeError("recovered must be a recovered report")
    if type(evidence) is not RetailReportEvidenceComparison:
        raise TypeError("evidence must be a report evidence comparison")
    if serialize_retail_rule_evaluation_report(evidence.report) != (
        serialize_retail_rule_evaluation_report(recovered.report)
    ):
        raise ValueError("evidence belongs to a different report")

    # Revalidate bindings instead of trusting a directly constructed container.
    validated = bind_retail_report_evidence_comparisons(
        report=recovered.report,
        expectations=tuple(
            item.expectation for item in evidence.references
            if item.expectation is not None
        ),
        comparisons=tuple(
            item.comparison for item in evidence.references
            if item.comparison is not None
        ),
    )
    if validated != evidence:
        raise ValueError("evidence references are incomplete or inconsistent")

    lines = [
        render_retail_vm_report_text(
            identity=identity, recovered=recovered,
        ).rstrip("\n"),
        "",
        "COMPROBACIONES DE ARCHIVOS DE EVIDENCIA",
        "Resultados de lecturas suministradas; esta presentación no abre archivos.",
        "Una coincidencia no acredita autenticidad, aprobación ni veracidad física.",
        "El archivo puede cambiar después de la lectura.",
    ]
    if not validated.references:
        lines.append("Sin referencias de evidencia declaradas.")
    for reference in validated.references:
        lines.extend([
            "",
            f"Evidencia: {_text(reference.evidence_id)}",
            f"Comprobación: {_LABELS[reference.status]}",
        ])
        expected = reference.expectation
        if expected is not None:
            lines.extend([
                f"Versión declarada: {_text(expected.identity.source_version)}",
                f"Tamaño esperado (bytes): {expected.byte_length}",
                "SHA-256 esperado: "
                + expected.identity.source_content_digest.value,
            ])
        comparison = reference.comparison
        if comparison is not None and comparison.observed_byte_length is not None:
            lines.append(
                f"Tamaño observado (bytes): {comparison.observed_byte_length}"
            )
        if comparison is not None and comparison.observed_digest is not None:
            lines.append("SHA-256 observado: " + comparison.observed_digest.value)
    return "\n".join(lines) + "\n"
