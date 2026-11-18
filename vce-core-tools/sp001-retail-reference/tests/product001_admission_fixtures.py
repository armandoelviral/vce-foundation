"""Shared PRODUCT-001 planogram admission test fixtures."""

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from test_knowledge_source_retrieval import (
    create_status,
    evaluate,
)
from test_retail_expected_state import create_snapshot
from test_retail_expected_state_rule import create_rule

from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeSourceRetrievalDecision,
)
from sp001.contracts.retail_context_observation_provenance import (
    RetailContextObservationProvenance,
)
from sp001.contracts.retail_context_observation_provenance_binding import (
    RetailContextObservationProvenanceBinding,
    bind_retail_context_observation_provenance,
)
from sp001.contracts.retail_context_snapshot import (
    RetailContextSnapshot,
)
from sp001.contracts.retail_expected_state_rule import (
    RetailExpectedStateRule,
)


@dataclass(frozen=True, slots=True)
class AdmissionCase:
    decision: KnowledgeSourceRetrievalDecision
    snapshot: RetailContextSnapshot
    rule: RetailExpectedStateRule
    bindings: tuple[
        RetailContextObservationProvenanceBinding, ...
    ]
    planogram_dimension_ids: tuple[str, ...]


def make_valid_admission_case() -> AdmissionCase:
    source = create_status()
    decision = evaluate(source=source)
    context = decision.retrieval_context

    original = create_snapshot()

    definition = replace(
        original.context_definition,
        customer_id=context.customer_id,
    )

    scope = replace(
        original.context_scope,
        commercial_channel_id=context.commercial_channel_id,
        point_of_sale_id=context.point_of_sale_id,
        department_id=context.department_id,
    )

    snapshot = replace(
        original,
        context_definition=definition,
        context_scope=scope,
    )

    rule = create_rule(
        context_definition=definition,
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

    return AdmissionCase(
        decision=decision,
        snapshot=snapshot,
        rule=rule,
        bindings=(binding,),
        planogram_dimension_ids=("DIM-DEPARTMENT-001",),
    )
