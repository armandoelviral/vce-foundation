import json

from sp001.services.recovered_retail_rule_evaluation_report import (
    RecoveredRetailRuleEvaluationReport,
)


def _text(value):
    # Keep user-supplied text on one line, preserving its literal content.
    return json.dumps(value, ensure_ascii=False)


def render_retail_vm_report_text(
    *, identity, recovered: RecoveredRetailRuleEvaluationReport,
) -> str:
    """Present supplied recovered content; performs no authorization or inspection."""
    from sp001.contracts.retail_rule_evaluation_report_store import (
        RetailRuleEvaluationReportIdentity,
    )
    if type(identity) is not RetailRuleEvaluationReportIdentity:
        raise TypeError("identity must be a report identity")
    if type(recovered) is not RecoveredRetailRuleEvaluationReport:
        raise TypeError("recovered must be a recovered report")

    report = recovered.report
    admissions = {
        item.evaluation.evaluation_id: item for item in recovered.admissions
    }
    lines = [
        "REPORTE DE REVISIÓN VM",
        f"Reporte solicitado: {_text(identity.report_id)}",
        f"Caso: {_text(report.case_id)}",
        "",
        "Alcance: evaluaciones declaradas y admisiones locales registradas.",
        "La admisión no equivale a aprobación de la composición.",
        "Las referencias de evidencia no acreditan archivos verificados.",
        "Este documento no verifica calibración, autenticidad ni integridad externa.",
    ]
    for evaluation in report.evaluations:
        observation = evaluation.observation
        criterion = evaluation.criterion
        actor = evaluation.evaluator
        lines.extend([
            "",
            f"Evaluación: {_text(evaluation.evaluation_id)}",
            f"Regla: {_text(criterion.rule_id)}",
            f"Versión del criterio: {criterion.criterion_version}",
            f"Criterio: {_text(criterion.statement)}",
            f"Resultado declarado: {observation.status.value}",
            f"Fundamento: {_text(evaluation.rationale)}",
            f"Observación: {_text(observation.observation_id)}",
            f"Snapshot: {_text(observation.snapshot_id)}",
            f"Versión del snapshot: {observation.snapshot_version}",
            f"Evaluador declarado: {_text(actor.actor_id)}",
            f"Tipo de actor: {actor.actor_type.value}",
            f"Cliente: {_text(actor.customer_id)}",
            f"Organización: {_text(actor.organization_id)}",
            f"Rol: {_text(actor.role.role_id)} / {_text(actor.role.role_name)}",
            f"Fecha declarada de evaluación: {evaluation.evaluated_at.isoformat()}",
            "Referencias de evidencia: " + _text(list(observation.evidence_ids)),
        ])
        admission = admissions.get(evaluation.evaluation_id)
        if admission is None:
            lines.append("Atribución: DECLARADA; sin admisión local recuperada.")
        else:
            binding = admission.binding_snapshot.binding
            lines.extend([
                "Atribución: ADMISIÓN LOCAL REGISTRADA.",
                f"Emisor del principal: {_text(admission.principal.issuer)}",
                f"Sujeto del principal: {_text(admission.principal.subject)}",
                f"Vinculación: {_text(binding.binding_id)}",
                f"Revisión utilizada: {binding.revision}",
                f"Instante de validación (Unix s): {admission.validated_at}",
                "La vigencia actual de esa vinculación no se infiere del historial.",
            ])

    lines.extend(["", "RELACIONES DECLARADAS"])
    if not report.relations:
        lines.append("Sin relaciones declaradas.")
    for relation in report.relations:
        lines.extend([
            f"Relación: {_text(relation.relation_id)}",
            f"Tipo: {relation.relation_type.value}",
            f"Anterior: {_text(relation.previous.evaluation_id)}",
            f"Actual: {_text(relation.current.evaluation_id)}",
            f"Fundamento: {_text(relation.rationale)}",
            "Evidencia de intervención: "
            + _text(list(relation.intervention_evidence_ids)),
        ])
    lines.append("Las relaciones no demuestran causalidad física.")
    return "\n".join(lines) + "\n"
