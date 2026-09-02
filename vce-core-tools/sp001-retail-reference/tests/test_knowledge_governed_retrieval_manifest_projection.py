import ast

from pathlib import Path

import pytest

from sp001.services.knowledge_governed_retrieval_manifest_projection import (
    project_knowledge_retrieval_manifest,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_retrieval_context,
)
from test_knowledge_candidate_lexical_matching import (
    create_included_candidate,
)
from test_knowledge_governed_retrieval import (
    execute,
)
from test_knowledge_retrieval_manifest import (
    create_candidate,
)


def create_manifest(*candidates):
    return execute(
        *candidates,
    ).manifest


def create_mixed_manifest():
    return create_manifest(
        create_included_candidate(
            candidate_id="CANDIDATE-INCLUDED",
            source_id="SOURCE-INCLUDED",
            content=b"governed planogram",
        ),
        create_candidate(
            candidate_id="CANDIDATE-EXCLUDED",
            source_id="SOURCE-EXCLUDED",
            included=False,
        ),
    )


def project(*candidates):
    return project_knowledge_retrieval_manifest(
        manifest=create_manifest(
            *candidates,
        ),
    )


def test_projection_requires_validated_manifest() -> None:
    with pytest.raises(
        TypeError,
        match="manifest must be a KnowledgeRetrievalManifest",
    ):
        project_knowledge_retrieval_manifest(
            manifest="manifest",  # type: ignore[arg-type]
        )


def test_manifest_projection_has_exact_root_fields() -> None:
    assert set(project()) == {
        "retrieval_context",
        "candidate_decisions",
    }


def test_empty_manifest_preserves_empty_candidate_universe() -> None:
    document = project()

    assert document["candidate_decisions"] == []


def test_manifest_context_uses_shared_projection() -> None:
    manifest = create_manifest()
    document = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )

    assert document["retrieval_context"] == (
        project_knowledge_retrieval_context(
            context=manifest.retrieval_context,
        )
    )


def test_candidate_decisions_preserve_declared_order() -> None:
    document = project_knowledge_retrieval_manifest(
        manifest=create_mixed_manifest(),
    )

    assert [
        candidate["candidate_id"]
        for candidate in document["candidate_decisions"]
    ] == [
        "CANDIDATE-INCLUDED",
        "CANDIDATE-EXCLUDED",
    ]


def test_candidate_projection_has_exact_fields() -> None:
    candidate = project_knowledge_retrieval_manifest(
        manifest=create_mixed_manifest(),
    )["candidate_decisions"][0]

    assert set(candidate) == {
        "candidate_id",
        "decision",
    }


def test_decision_projection_has_exact_fields() -> None:
    decision = project_knowledge_retrieval_manifest(
        manifest=create_mixed_manifest(),
    )["candidate_decisions"][0]["decision"]

    assert set(decision) == {
        "source_status",
        "retrieval_context",
        "content_bytes_match_digest",
        "scope_evaluation",
        "temporal_evaluation",
        "verified_authority_binding_ids",
        "supersession_ids",
        "decision_status",
        "exclusion_reasons",
    }


def test_source_status_projection_is_complete() -> None:
    manifest = create_mixed_manifest()
    status = manifest.candidate_decisions[0].decision.source_status
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"]["source_status"]

    assert set(projected) == {
        "status_record_id",
        "status_version",
        "identity",
        "scope",
        "lifecycle_status",
        "evidence_status",
    }
    assert projected["status_record_id"] == status.status_record_id
    assert projected["status_version"] == status.status_version
    assert projected["lifecycle_status"] == (
        status.lifecycle_status.value
    )
    assert projected["evidence_status"] == (
        status.evidence_status.value
    )


def test_source_identity_and_digest_are_complete() -> None:
    manifest = create_mixed_manifest()
    identity = (
        manifest.candidate_decisions[0]
        .decision.source_status.identity
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"][
        "source_status"
    ]["identity"]

    assert projected == {
        "source_id": identity.source_id,
        "source_version": identity.source_version,
        "source_content_digest": {
            "algorithm": (
                identity.source_content_digest.algorithm
            ),
            "value": identity.source_content_digest.value,
        },
    }


def test_source_scope_projection_is_complete() -> None:
    manifest = create_mixed_manifest()
    scope = (
        manifest.candidate_decisions[0]
        .decision.source_status.scope
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"][
        "source_status"
    ]["scope"]

    assert projected == {
        "organization_id": scope.organization_id,
        "customer_id": scope.customer_id,
        "jurisdiction": scope.jurisdiction,
        "commercial_channel_id": scope.commercial_channel_id,
        "document_type": scope.document_type.value,
        "point_of_sale_scope": {
            "mode": scope.point_of_sale_scope.mode.value,
            "ids": list(scope.point_of_sale_scope.ids),
        },
        "department_scope": {
            "mode": scope.department_scope.mode.value,
            "ids": list(scope.department_scope.ids),
        },
        "campaign_id": scope.campaign_id,
    }


def test_scope_selection_ids_preserve_declared_order() -> None:
    manifest = create_mixed_manifest()
    scope = (
        manifest.candidate_decisions[0]
        .decision.source_status.scope
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"][
        "source_status"
    ]["scope"]

    assert projected["point_of_sale_scope"]["ids"] == list(
        scope.point_of_sale_scope.ids
    )
    assert projected["department_scope"]["ids"] == list(
        scope.department_scope.ids
    )


def test_scope_evaluation_projection_is_complete() -> None:
    manifest = create_mixed_manifest()
    evaluation = (
        manifest.candidate_decisions[1]
        .decision.scope_evaluation
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][1]["decision"][
        "scope_evaluation"
    ]

    assert projected["match_status"] == (
        evaluation.match_status.value
    )
    assert projected["mismatch_reasons"] == [
        reason.value
        for reason in evaluation.mismatch_reasons
    ]
    assert projected["retrieval_context"] == (
        project_knowledge_retrieval_context(
            context=evaluation.retrieval_context,
        )
    )


def test_temporal_evaluation_projection_is_complete() -> None:
    manifest = create_mixed_manifest()
    evaluation = (
        manifest.candidate_decisions[0]
        .decision.temporal_evaluation
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"][
        "temporal_evaluation"
    ]

    assert projected["evaluated_at"] == (
        evaluation.evaluated_at.isoformat()
    )
    assert projected["temporal_status"] == (
        evaluation.temporal_status.value
    )


def test_effective_period_projection_is_complete() -> None:
    manifest = create_mixed_manifest()
    period = (
        manifest.candidate_decisions[0]
        .decision.temporal_evaluation.effective_period
    )
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"][
        "temporal_evaluation"
    ]["effective_period"]

    assert projected["effective_from"] == (
        period.effective_from.isoformat()
    )
    assert projected["effective_until"] == (
        period.effective_until.isoformat()
        if period.effective_until is not None
        else None
    )
    assert projected["source_status"]["identity"][
        "source_id"
    ] == period.source_status.identity.source_id


def test_authority_binding_ids_preserve_declared_order() -> None:
    manifest = create_mixed_manifest()
    decision = manifest.candidate_decisions[0].decision
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"]

    assert projected["verified_authority_binding_ids"] == list(
        decision.verified_authority_binding_ids
    )


def test_supersession_ids_preserve_declared_order() -> None:
    manifest = create_mixed_manifest()
    decision = manifest.candidate_decisions[0].decision
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][0]["decision"]

    assert projected["supersession_ids"] == list(
        decision.supersession_ids
    )


def test_decision_status_uses_declared_enum_value() -> None:
    manifest = create_mixed_manifest()
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"]

    assert [
        candidate["decision"]["decision_status"]
        for candidate in projected
    ] == [
        candidate.decision.decision_status.value
        for candidate in manifest.candidate_decisions
    ]


def test_exclusion_reasons_preserve_declared_order() -> None:
    manifest = create_mixed_manifest()
    decision = manifest.candidate_decisions[1].decision
    projected = project_knowledge_retrieval_manifest(
        manifest=manifest,
    )["candidate_decisions"][1]["decision"]

    assert projected["exclusion_reasons"] == [
        reason.value
        for reason in decision.exclusion_reasons
    ]


def test_projection_contains_only_json_compatible_values() -> None:
    document = project_knowledge_retrieval_manifest(
        manifest=create_mixed_manifest(),
    )

    def assert_compatible(value) -> None:
        if isinstance(
            value,
            dict,
        ):
            assert all(
                isinstance(key, str)
                for key in value
            )
            for nested in value.values():
                assert_compatible(nested)
            return
        if isinstance(
            value,
            list,
        ):
            for nested in value:
                assert_compatible(nested)
            return
        assert value is None or type(value) in {
            str,
            int,
            bool,
        }

    assert_compatible(document)


def test_projection_uses_no_generic_or_premature_serialization() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval_manifest_projection.py"
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    forbidden_names = {
        "asdict",
        "fields",
        "is_dataclass",
        "json",
        "hashlib",
    }

    assert not (
        forbidden_names
        & {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
    )
    assert "serialize" not in source
    assert "digest_knowledge_governed" not in source
