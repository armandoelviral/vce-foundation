"""PRODUCT-001: initial planogram admission interface tests."""

import pytest

from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
)


def test_admission_contract_vocabulary_exists() -> None:
    assert KnowledgeRetrievalDecisionStatus.INCLUDED.value == "INCLUDED"
    assert KnowledgeRetrievalDecisionStatus.EXCLUDED.value == "EXCLUDED"
    assert KnowledgeDocumentType.PLANOGRAM.value == "PLANOGRAM"


def test_product001_admission_adapter_is_importable() -> None:
    from sp001.services.product001_planogram_admission import (
        generate_admitted_planogram_expected_state,
    )

    assert callable(generate_admitted_planogram_expected_state)


def test_product001_positive_provenance_composition() -> None:
    """Document provenance binds to the exact matched dimension."""
    from dataclasses import replace
    from datetime import datetime, timezone

    from test_knowledge_source_retrieval import (
        create_status,
        evaluate,
    )
    from test_retail_expected_state import create_snapshot
    from test_retail_expected_state_rule import create_rule

    from sp001.contracts.knowledge_retrieval_decision import (
        KnowledgeRetrievalDecisionStatus,
    )
    from sp001.contracts.retail_context_observation_provenance import (
        RetailContextObservationProvenance,
    )
    from sp001.contracts.retail_context_observation_provenance_binding import (
        bind_retail_context_observation_provenance,
    )
    from sp001.contracts.retail_expected_state_rule_evaluation import (
        ExpectedStateRuleEvaluationStatus,
        evaluate_retail_expected_state_rule,
    )

    source = create_status()
    decision = evaluate(source=source)
    context = decision.retrieval_context

    original_snapshot = create_snapshot()

    definition = replace(
        original_snapshot.context_definition,
        customer_id=context.customer_id,
    )
    scope = replace(
        original_snapshot.context_scope,
        commercial_channel_id=context.commercial_channel_id,
        point_of_sale_id=context.point_of_sale_id,
        department_id=context.department_id,
    )
    snapshot = replace(
        original_snapshot,
        context_definition=definition,
        context_scope=scope,
    )
    rule = create_rule(context_definition=definition)

    evaluation = evaluate_retail_expected_state_rule(
        rule=rule,
        snapshot=snapshot,
    )

    observed_at = datetime(
        2026, 3, 15, 12, tzinfo=timezone.utc
    )

    provenance = RetailContextObservationProvenance(
        observation_id="PRODUCT-001-OBS-001",
        observation_version=1,
        case_id=snapshot.case_id,
        snapshot_id=snapshot.snapshot_id,
        snapshot_version=snapshot.snapshot_version,
        dimension_id="DIM-DEPARTMENT-001",
        source_identity=source.identity,
        observed_at=observed_at,
        recorded_at=observed_at,
        effective_from=observed_at,
        evidence_ids=("PRODUCT-001-EVIDENCE-001",),
    )

    binding = bind_retail_context_observation_provenance(
        snapshot=snapshot,
        provenance=provenance,
    )

    assert (
        decision.decision_status
        is KnowledgeRetrievalDecisionStatus.INCLUDED
    )
    assert (
        evaluation.status
        is ExpectedStateRuleEvaluationStatus.APPLICABLE
    )
    assert binding.snapshot is snapshot
    assert binding.provenance.source_identity == source.identity
    assert binding.dimension.dimension_id == "DIM-DEPARTMENT-001"
    assert binding.dimension.dimension_id in evaluation.matched_dimension_ids
    assert "DIM-INVENTORY-001" in evaluation.matched_dimension_ids
    assert binding.dimension.dimension_id != "DIM-INVENTORY-001"
