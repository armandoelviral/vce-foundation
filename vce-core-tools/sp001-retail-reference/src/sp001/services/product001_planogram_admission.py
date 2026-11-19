"""PRODUCT-001 planogram expected-state admission boundary."""

from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeSourceRetrievalDecision,
)
from sp001.contracts.knowledge_source_scope import KnowledgeDocumentType
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
)
from sp001.contracts.retail_context_snapshot import RetailContextSnapshot
from sp001.contracts.retail_expected_state import RetailExpectedState
from sp001.contracts.retail_expected_state_rule import RetailExpectedStateRule
from sp001.contracts.retail_expected_state_rule_evaluation import (
    ExpectedStateRuleEvaluationStatus,
    evaluate_retail_expected_state_rule,
)
from sp001.services.retail_expected_state_generation import (
    generate_retail_expected_state,
)


def _compose_planogram_expected_state_from_decision(
    *,
    expected_state_id: str,
    expected_state_version: int,
    rule: RetailExpectedStateRule,
    snapshot: RetailContextSnapshot,
    retrieval_decision: KnowledgeSourceRetrievalDecision,
    provenance_bindings: tuple[
        RetailContextObservationProvenanceBinding, ...
    ],
    planogram_dimension_ids: tuple[str, ...],
) -> RetailExpectedState:
    """Generate only after checking documentary/contextual composition."""

    if not isinstance(retrieval_decision, KnowledgeSourceRetrievalDecision):
        raise TypeError("retrieval_decision has invalid type")
    if not isinstance(snapshot, RetailContextSnapshot):
        raise TypeError("snapshot has invalid type")
    if not isinstance(rule, RetailExpectedStateRule):
        raise TypeError("rule has invalid type")

    if retrieval_decision.decision_status is not KnowledgeRetrievalDecisionStatus.INCLUDED:
        raise ValueError("excluded source cannot authorize admission")

    if retrieval_decision.content_bytes_match_digest is not True:
        raise ValueError("source content digest mismatch")

    source = retrieval_decision.source_status
    context = retrieval_decision.retrieval_context

    if (
        source.scope.document_type is not KnowledgeDocumentType.PLANOGRAM
        or context.document_type is not KnowledgeDocumentType.PLANOGRAM
    ):
        raise ValueError("document must be a PLANOGRAM")

    if snapshot.context_definition is None:
        raise ValueError("customer context definition is required")
    if snapshot.context_scope is None:
        raise ValueError("retail context scope is required")

    if snapshot.context_definition.customer_id != context.customer_id:
        raise ValueError("customer mismatch")
    if (
        snapshot.context_scope.commercial_channel_id
        != context.commercial_channel_id
    ):
        raise ValueError("channel mismatch")
    if snapshot.context_scope.point_of_sale_id != context.point_of_sale_id:
        raise ValueError("point of sale mismatch")
    if snapshot.context_scope.department_id != context.department_id:
        raise ValueError("department mismatch")

    evaluation = evaluate_retail_expected_state_rule(
        rule=rule,
        snapshot=snapshot,
    )
    if evaluation.status is not ExpectedStateRuleEvaluationStatus.APPLICABLE:
        raise ValueError("rule is not applicable")

    if (
        not isinstance(planogram_dimension_ids, tuple)
        or not planogram_dimension_ids
        or any(
            not isinstance(dimension_id, str) or not dimension_id.strip()
            for dimension_id in planogram_dimension_ids
        )
        or len(set(planogram_dimension_ids)) != len(planogram_dimension_ids)
    ):
        raise ValueError("dimension selection must be nonempty and unique")

    for dimension_id in planogram_dimension_ids:
        if dimension_id not in evaluation.matched_dimension_ids:
            raise ValueError("dimension not matched by applicable rule")

    if not isinstance(provenance_bindings, tuple):
        raise TypeError("provenance_bindings must be a tuple")

    for binding in provenance_bindings:
        if not isinstance(binding, RetailContextObservationProvenanceBinding):
            raise TypeError("invalid provenance binding")
        if binding.snapshot is not snapshot:
            raise ValueError("snapshot binding mismatch")

    binding_dimension_ids = tuple(
        binding.dimension.dimension_id
        for binding in provenance_bindings
    )

    if (
        len(binding_dimension_ids) != len(planogram_dimension_ids)
        or set(binding_dimension_ids) != set(planogram_dimension_ids)
    ):
        raise ValueError("binding dimension set mismatch")

    expected_identity = source.identity

    for dimension_id in planogram_dimension_ids:
        candidates = [
            binding
            for binding in provenance_bindings
            if binding.dimension.dimension_id == dimension_id
        ]

        if len(candidates) != 1:
            raise ValueError("exactly one binding required per dimension")

        identity = candidates[0].provenance.source_identity

        if identity.source_id != expected_identity.source_id:
            raise ValueError("source identity mismatch")
        if identity.source_version != expected_identity.source_version:
            raise ValueError("source version mismatch")
        if (
            identity.source_content_digest
            != expected_identity.source_content_digest
        ):
            raise ValueError("source identity digest mismatch")

    return generate_retail_expected_state(
        expected_state_id=expected_state_id,
        expected_state_version=expected_state_version,
        rule=rule,
        snapshot=snapshot,
    )


def generate_admitted_planogram_expected_state(
    *,
    expected_state_id,
    expected_state_version,
    rule,
    snapshot,
    retrieval_decision,
    provenance_bindings,
    planogram_dimension_ids,
):
    """Reject caller-supplied admission decisions."""
    raise ValueError(
        "untrusted admission authority: "
        "caller-supplied retrieval decisions cannot authorize generation"
    )
