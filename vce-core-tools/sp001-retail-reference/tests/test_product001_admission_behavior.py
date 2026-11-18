"""Behavioral RED tests for PRODUCT-001 admission."""

import pytest

from product001_admission_fixtures import (
    make_valid_admission_case,
)
from test_knowledge_source_retrieval import evaluate

from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)


def call_admission(case):
    from sp001.services.product001_planogram_admission import (
        generate_admitted_planogram_expected_state,
    )

    return generate_admitted_planogram_expected_state(
        expected_state_id="PRODUCT-001-EXPECTED-001",
        expected_state_version=1,
        rule=case.rule,
        snapshot=case.snapshot,
        retrieval_decision=case.decision,
        provenance_bindings=case.bindings,
        planogram_dimension_ids=case.planogram_dimension_ids,
    )


def test_valid_admission_generates_expected_state():
    case = make_valid_admission_case()

    state = call_admission(case)

    assert state.snapshot is case.snapshot
    assert state.expected_state_id == "PRODUCT-001-EXPECTED-001"
    assert "DIM-DEPARTMENT-001" in state.source_dimension_ids
    assert "DIM-INVENTORY-001" in state.source_dimension_ids


def test_excluded_source_is_rejected():
    from dataclasses import replace

    case = make_valid_admission_case()

    excluded = evaluate(
        source=case.decision.source_status,
        content=b"tampered planogram content",
    )

    assert (
        excluded.decision_status
        is KnowledgeRetrievalDecisionStatus.EXCLUDED
    )
    assert excluded.content_bytes_match_digest is False

    invalid_case = replace(case, decision=excluded)

    with pytest.raises(ValueError, match="(?i)excluded"):
        call_admission(invalid_case)



def altered_provenance_case(*, source_id=None, source_version=None):
    from dataclasses import replace

    from sp001.contracts.retail_context_observation_provenance_binding import (
        bind_retail_context_observation_provenance,
    )

    case = make_valid_admission_case()
    original_binding = case.bindings[0]
    identity = original_binding.provenance.source_identity

    altered_identity = replace(
        identity,
        source_id=(
            source_id if source_id is not None
            else identity.source_id
        ),
        source_version=(
            source_version if source_version is not None
            else identity.source_version
        ),
    )

    provenance = replace(
        original_binding.provenance,
        source_identity=altered_identity,
    )

    binding = bind_retail_context_observation_provenance(
        snapshot=case.snapshot,
        provenance=provenance,
    )

    return replace(case, bindings=(binding,))


def test_wrong_source_identity_is_rejected():
    case = altered_provenance_case(
        source_id="POG-OTHER-SOURCE",
    )

    assert (
        case.bindings[0].provenance.source_identity.source_id
        != case.decision.source_status.identity.source_id
    )

    with pytest.raises(ValueError, match="(?i)identity"):
        call_admission(case)


def test_wrong_source_version_is_rejected():
    case = altered_provenance_case(
        source_version="obsolete",
    )

    assert (
        case.bindings[0].provenance.source_identity.source_version
        != case.decision.source_status.identity.source_version
    )

    with pytest.raises(ValueError, match="(?i)version"):
        call_admission(case)


def test_missing_document_binding_is_rejected():
    from dataclasses import replace

    case = replace(
        make_valid_admission_case(),
        bindings=(),
    )

    assert case.bindings == ()
    assert case.planogram_dimension_ids == (
        "DIM-DEPARTMENT-001",
    )

    with pytest.raises(ValueError, match="(?i)binding"):
        call_admission(case)



def test_wrong_document_type_is_rejected():
    from dataclasses import replace
    from datetime import datetime, timezone

    from test_knowledge_source_retrieval import create_binding
    from sp001.contracts.knowledge_source_scope import KnowledgeDocumentType
    from sp001.contracts.knowledge_source_effective_period import (
        KnowledgeSourceEffectivePeriod,
    )
    from sp001.contracts.knowledge_source_supersession import (
        KnowledgeSourceSupersessionGraph,
    )
    from sp001.services.knowledge_source_retrieval import (
        evaluate_knowledge_source_retrieval,
    )

    case = make_valid_admission_case()
    source = replace(
        case.decision.source_status,
        scope=replace(
            case.decision.source_status.scope,
            document_type=KnowledgeDocumentType.LOOKBOOK,
        ),
    )
    context = replace(
        case.decision.retrieval_context,
        document_type=KnowledgeDocumentType.LOOKBOOK,
    )
    decision = evaluate_knowledge_source_retrieval(
        source_status=source,
        content=b"approved denim planogram",
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=source,
            effective_from=datetime(2026, 3, 1, tzinfo=timezone.utc),
        ),
        retrieval_context=context,
        authority_bindings=(create_binding(source),),
        supersession_graph=KnowledgeSourceSupersessionGraph(
            supersessions=(),
        ),
    )
    assert decision.decision_status is KnowledgeRetrievalDecisionStatus.INCLUDED
    with pytest.raises(ValueError, match="(?i)planogram|document"):
        call_admission(replace(case, decision=decision))


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    (
        ("customer", "FOREIGN-CUSTOMER", "customer"),
        ("channel", "FOREIGN-CHANNEL", "channel"),
        ("store", "FOREIGN-STORE", "store|point.of.sale"),
        ("department", "FOREIGN-DEPARTMENT", "department"),
    ),
)
def test_foreign_retail_context_is_rejected(field, replacement, message):
    from dataclasses import replace

    case = make_valid_admission_case()
    snapshot = case.snapshot

    if field == "customer":
        snapshot = replace(
            snapshot,
            context_definition=replace(
                snapshot.context_definition,
                customer_id=replacement,
            ),
        )
    else:
        attribute = {
            "channel": "commercial_channel_id",
            "store": "point_of_sale_id",
            "department": "department_id",
        }[field]
        snapshot = replace(
            snapshot,
            context_scope=replace(
                snapshot.context_scope,
                **{attribute: replacement},
            ),
        )

    with pytest.raises(ValueError, match=f"(?i){message}"):
        call_admission(replace(case, snapshot=snapshot))


def test_foreign_snapshot_binding_is_rejected():
    from dataclasses import replace
    from sp001.contracts.retail_context_observation_provenance_binding import (
        bind_retail_context_observation_provenance,
    )

    case = make_valid_admission_case()
    foreign = replace(case.snapshot, snapshot_id="FOREIGN-SNAPSHOT")
    provenance = replace(
        case.bindings[0].provenance,
        snapshot_id="FOREIGN-SNAPSHOT",
    )
    binding = bind_retail_context_observation_provenance(
        snapshot=foreign,
        provenance=provenance,
    )
    assert binding.snapshot is not case.snapshot

    with pytest.raises(ValueError, match="(?i)snapshot|binding"):
        call_admission(replace(case, bindings=(binding,)))


def test_unmatched_document_dimension_is_rejected():
    from dataclasses import replace

    case = replace(
        make_valid_admission_case(),
        planogram_dimension_ids=("DIM-UNMATCHED",),
    )
    with pytest.raises(ValueError, match="(?i)dimension"):
        call_admission(case)


def test_inapplicable_rule_is_rejected():
    from dataclasses import replace

    case = make_valid_admission_case()
    rule = replace(
        case.rule,
        required_dimension_values=(
            ("DEPARTMENT", "IMPOSSIBLE-DEPARTMENT-VALUE"),
        ),
    )
    with pytest.raises(ValueError, match="(?i)rule|applicable"):
        call_admission(replace(case, rule=rule))
