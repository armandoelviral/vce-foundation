from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]

MODEL = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_ARCHITECTURE_LAYER_MODEL.md"
)

FREEZE = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_ARCHITECTURE_RESPONSIBILITY_FREEZE.md"
)

CYCLE_1 = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_REFUTATION_CYCLE_1.md"
)

CYCLE_2 = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_REFUTATION_CYCLE_2_TARGETED_RESPONSIBILITIES.md"
)

CYCLE_3 = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_REFUTATION_CYCLE_3_PLACEMENT_TOPOLOGY_IDENTITY.md"
)

CYCLE_4 = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_layers"
    / "ALM001_REFUTATION_CYCLE_4_FINAL_MINIMALITY.md"
)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(content: str) -> str:
    return " ".join(content.split())


def model_text() -> str:
    return text(MODEL)


def freeze_text() -> str:
    return text(FREEZE)


def section(content: str, start: str, end: str) -> str:
    return content[
        content.index(start):
        content.index(end)
    ]


def enum_values(content: str, start: str, end: str) -> list[str]:
    block = section(content, start, end)

    return re.findall(
        r"^([A-Z][A-Z_]+)\.$",
        block,
        flags=re.MULTILINE,
    )


def test_required_alm001_artifacts_exist() -> None:
    for path in (
        MODEL,
        FREEZE,
        CYCLE_1,
        CYCLE_2,
        CYCLE_3,
        CYCLE_4,
    ):
        assert path.is_file(), f"missing ALM-001 artifact: {path}"


def test_alm001_identity() -> None:
    content = normalized(model_text())

    assert "Identifier ALM-001." in content
    assert "Version 1.0." in content
    assert "Status Normative." in content
    assert "Architecture Responsibility Baseline." in content


def test_alm001_declares_promoted_authority() -> None:
    content = normalized(model_text())

    assert "Baseline 1.0." in content
    assert "Authority AUTHORITATIVE." in content
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_alm001_preserves_promoted_source_identity() -> None:
    content = normalized(model_text())

    assert "Source Candidate ALM-001 Version 0.4." in content


def test_architecture_is_not_linear_hierarchy() -> None:
    content = normalized(model_text())

    assert (
        "Architecture shall be represented through explicit responsibility "
        "dimensions rather than a mandatory vertical hierarchy."
        in content
    )


def test_architecture_participation_does_not_imply_authority() -> None:
    content = normalized(model_text())

    for item in (
        "Normative authority.",
        "Ownership.",
        "Precedence.",
        "Containment.",
        "Execution order.",
        "Lifecycle order.",
        "Repository hierarchy.",
    ):
        assert item in content


def test_architecture_context_is_explicit() -> None:
    content = normalized(model_text())

    assert (
        "Every architectural classification shall occur within an explicit "
        "Architecture Context."
        in content
    )


def test_responsibility_identity_is_semantic_not_physical() -> None:
    content = normalized(model_text())

    for forbidden_identity_source in (
        "Filename.",
        "Repository path.",
        "Component name.",
        "Implementation class.",
        "Programming language.",
        "Process identity.",
        "Deployment unit.",
    ):
        assert forbidden_identity_source in content


def test_implementation_relocation_does_not_create_new_identity() -> None:
    content = normalized(model_text())

    assert (
        "Implementation relocation shall not by itself create new identity."
        in content
    )


def test_renaming_does_not_create_new_identity() -> None:
    content = normalized(model_text())

    assert "Renaming shall not by itself create new identity." in content


def test_multi_dimensional_participation_is_explicit() -> None:
    content = normalized(model_text())

    assert (
        "One architectural entity may participate in multiple "
        "responsibility dimensions."
        in content
    )

    assert (
        "Classification shall not be forced into one exclusive dimension"
        in content
    )


def test_alm001_declares_exactly_eight_responsibility_dimensions() -> None:
    values = enum_values(
        model_text(),
        "## Retained Responsibility Dimensions",
        "## Shared Architecture",
    )

    assert values == [
        "SHARED_ARCHITECTURE",
        "DOMAIN_ARCHITECTURE",
        "RUNTIME_ARCHITECTURE",
        "ARTIFACT_ARCHITECTURE",
        "SECURITY_ARCHITECTURE",
        "DATA_ARCHITECTURE",
        "INTEGRATION_ARCHITECTURE",
        "PLACEMENT_ARCHITECTURE",
    ]


def test_responsibility_dimensions_are_not_mandatory_or_hierarchical() -> None:
    content = normalized(model_text())

    assert "These dimensions are not:" in content
    assert "Mandatory." in content
    assert "Mutually exclusive." in content
    assert "Hierarchically ordered." in content
    assert "Normatively authoritative." in content


def test_shared_architecture_is_context_relative() -> None:
    content = normalized(model_text())

    assert "Shared status shall remain context-relative." in content


def test_shared_architecture_does_not_imply_universality_or_authority() -> None:
    content = normalized(model_text())

    for item in (
        "Universality.",
        "Authority.",
        "Superiority.",
        "Mandatory adoption.",
    ):
        assert item in content


def test_domain_architecture_requires_meaningful_domain_boundary() -> None:
    content = normalized(model_text())

    assert (
        "Naming something a domain shall not establish Domain Architecture."
        in content
    )


def test_runtime_architecture_requires_execution_responsibility() -> None:
    content = normalized(model_text())

    assert "Executability alone shall not establish Runtime Architecture." in content


def test_artifact_architecture_is_not_file_existence() -> None:
    content = normalized(model_text())

    assert (
        "File existence or versionability alone shall not establish "
        "Artifact Architecture."
        in content
    )


def test_security_architecture_requires_primary_security_responsibility() -> None:
    content = normalized(model_text())

    assert "Incidental security relevance shall not be sufficient." in content


def test_data_architecture_requires_independent_data_responsibility() -> None:
    content = normalized(model_text())

    assert (
        "Presence of data alone shall not establish Data Architecture."
        in content
    )


def test_data_architecture_does_not_require_persistence() -> None:
    content = normalized(model_text())

    assert "Persistence shall not be required." in content


def test_integration_architecture_requires_meaningful_boundary() -> None:
    content = normalized(model_text())

    assert (
        "Communication alone shall not establish Integration Architecture."
        in content
    )


def test_placement_architecture_requires_architectural_materiality() -> None:
    content = normalized(model_text())

    assert (
        "Ordinary deployment or operations mechanics shall not establish "
        "Placement Architecture unless they materially affect "
        "architectural correctness."
        in content
    )


def test_responsibility_independence_test_exists() -> None:
    content = normalized(model_text())

    assert "## Responsibility Independence Test" in model_text()

    for item in (
        "Semantic loss.",
        "Boundary confusion.",
        "Responsibility fragmentation.",
        "False ownership.",
        "False authority inference.",
    ):
        assert item in content


def test_alm001_declares_exactly_seven_relationship_types() -> None:
    values = enum_values(
        model_text(),
        "## Candidate Relationship Types",
        "## Relationship Scope",
    )

    assert values == [
        "USES",
        "REALIZES",
        "CONSTRAINS",
        "EXPOSES",
        "COMPOSES_WITH",
        "SPECIALIZES",
        "INTERSECTS",
    ]


def test_relationship_scope_is_explicit() -> None:
    content = normalized(model_text())

    assert (
        "Every architectural relationship shall possess explicit scope."
        in content
    )

    assert "Scope shall not silently expand." in content


def test_relationship_direction_does_not_imply_authority() -> None:
    content = normalized(model_text())

    for item in (
        "Normative authority.",
        "Precedence.",
        "Ownership.",
        "Lifecycle progression.",
        "Execution order.",
    ):
        assert item in content


def test_uses_is_not_inferred_from_import_or_invocation() -> None:
    content = normalized(model_text())

    for item in (
        "Import.",
        "Function call.",
        "Service invocation.",
        "Repository dependency.",
    ):
        assert item in content


def test_realizes_does_not_create_normative_source() -> None:
    content = normalized(model_text())

    assert (
        "Realization shall not make the realizing entity the normative source."
        in content
    )


def test_constrains_does_not_create_normative_authority() -> None:
    content = normalized(model_text())

    assert "CONSTRAINS shall not automatically create normative authority." in content


def test_exposes_is_distinct_from_uses() -> None:
    content = normalized(model_text())

    assert (
        "EXPOSES shall remain distinct from consumer-side USES semantics."
        in content
    )


def test_composes_with_does_not_imply_hierarchy() -> None:
    content = normalized(model_text())

    assert "Composition shall not imply hierarchy." in content


def test_specializes_does_not_create_normative_subordination() -> None:
    content = normalized(model_text())

    assert (
        "Specialization shall not automatically create normative subordination."
        in content
    )


def test_intersects_requires_explicit_overlap() -> None:
    content = normalized(model_text())

    assert "INTERSECTS shall require explicit overlap." in content
    assert "It shall not be used as a fallback for unknown relationships." in content


def test_no_relationship_state_is_valid() -> None:
    content = normalized(model_text())

    assert "No edge is a valid architecture-graph state." in content
    assert "The model shall not manufacture relationships for completeness." in content


def test_graph_minimality_rejects_repository_and_runtime_false_edges() -> None:
    content = normalized(model_text())

    for item in (
        "Repository co-location.",
        "Imports.",
        "Runtime invocation.",
        "Deployment co-location.",
        "Shared implementation.",
        "Historical association.",
        "Common ownership.",
        "Similar naming.",
    ):
        assert item in content


def test_shared_and_domain_architecture_are_distinct() -> None:
    content = normalized(model_text())

    assert (
        "Shared Architecture and Domain Architecture shall remain "
        "independently classifiable."
        in content
    )


def test_runtime_does_not_determine_domain_meaning() -> None:
    content = normalized(model_text())

    assert "Runtime realization shall not determine domain meaning." in content


def test_artifact_representation_does_not_determine_normative_meaning() -> None:
    content = normalized(model_text())

    assert "Artifact representation shall not determine normative meaning." in content


def test_security_incidental_consequence_does_not_force_classification() -> None:
    content = normalized(model_text())

    assert (
        "Incidental security consequence shall not force "
        "Security Architecture classification."
        in content
    )


def test_data_presence_does_not_force_data_architecture() -> None:
    content = normalized(model_text())

    assert (
        "Every system processing data shall not therefore automatically "
        "possess Data Architecture as a distinct classification."
        in content
    )


def test_internal_invocation_does_not_force_integration_architecture() -> None:
    content = normalized(model_text())

    assert (
        "Internal invocation alone shall not establish Integration Architecture."
        in content
    )


def test_placement_is_not_created_by_operational_mechanics() -> None:
    content = normalized(model_text())

    for item in (
        "Deployment event.",
        "Container count.",
        "Cloud provider.",
        "Orchestrator.",
        "Routine VM relocation.",
        "Operational rollout.",
    ):
        assert item in content


def test_cross_dimension_intersection_does_not_imply_subsumption_or_authority() -> None:
    content = normalized(model_text())

    for item in (
        "Subsumption.",
        "Ownership.",
        "Authority.",
        "Hierarchy.",
    ):
        assert item in content


def test_alm001_does_not_define_normative_authority() -> None:
    content = normalized(model_text())

    assert "ALM-001 shall not define normative authority." in content
    assert "Normative authority is governed through NAM-001." in content


def test_architectural_relationships_do_not_create_promotion_authority() -> None:
    content = normalized(model_text())

    for item in (
        "Promotion Authority.",
        "Conflict Resolution Authority.",
        "Authority precedence.",
        "Authority roots.",
        "Normative subordination.",
    ):
        assert item in content


def test_lifecycle_state_is_not_architecture_dimension() -> None:
    content = normalized(model_text())

    for item in (
        "Draft.",
        "Candidate.",
        "Validated.",
        "Promoted.",
        "Frozen.",
        "Superseded.",
        "Withdrawn.",
        "Refuted.",
    ):
        assert item in content


def test_processing_order_does_not_define_architecture() -> None:
    content = normalized(model_text())

    for item in (
        "Execution pipeline.",
        "Evidence pipeline.",
        "Replay pipeline.",
        "Validation pipeline.",
        "Certification pipeline.",
    ):
        assert item in content


def test_implementation_technology_does_not_define_architecture() -> None:
    content = normalized(model_text())

    for item in (
        "Programming language.",
        "Framework.",
        "Library.",
        "Vendor.",
        "Container platform.",
        "Cloud provider.",
        "Operating system.",
        "Database product.",
    ):
        assert item in content


def test_observability_remains_refuted_as_independent_dimension() -> None:
    content = normalized(model_text())

    assert "OBSERVABILITY_ARCHITECTURE" in content
    assert (
        "remains refuted as an independent responsibility dimension "
        "under current evidence."
        in content
    )


def test_rejected_placement_identities_are_not_peer_dimensions() -> None:
    content = normalized(model_text())

    for item in (
        "DEPLOYMENT_ARCHITECTURE.",
        "INFRASTRUCTURE_ARCHITECTURE.",
        "TOPOLOGY_ARCHITECTURE.",
    ):
        assert item in content

    retained = enum_values(
        model_text(),
        "## Retained Responsibility Dimensions",
        "## Shared Architecture",
    )

    assert "DEPLOYMENT_ARCHITECTURE" not in retained
    assert "INFRASTRUCTURE_ARCHITECTURE" not in retained
    assert "TOPOLOGY_ARCHITECTURE" not in retained


def test_placement_is_the_retained_placement_identity() -> None:
    retained = enum_values(
        model_text(),
        "## Retained Responsibility Dimensions",
        "## Shared Architecture",
    )

    assert "PLACEMENT_ARCHITECTURE" in retained


def test_taxonomy_does_not_claim_universal_completeness() -> None:
    content = normalized(model_text())

    assert "Version 0.4 does not claim universal completeness." in content


def test_taxonomy_remains_refutable() -> None:
    content = normalized(model_text())

    assert (
        "The current taxonomy shall remain subject to reduction."
        in content
    )


def test_relationship_taxonomy_remains_refutable() -> None:
    content = normalized(model_text())

    assert (
        "The seven relationship types shall remain subject to reduction."
        in content
    )


def test_post_promotion_observability_remains_non_authoritative() -> None:
    content = normalized(model_text())

    assert (
        "Observability Architecture NON-AUTHORITATIVE "
        "AS INDEPENDENT DIMENSION."
        in content
    )


def test_post_promotion_rejected_placement_identities_remain_non_authoritative() -> None:
    content = normalized(model_text())

    assert (
        "Rejected Placement Identities NON-AUTHORITATIVE "
        "AS PEER DIMENSIONS."
        in content
    )


def test_freeze_identity() -> None:
    content = normalized(freeze_text())

    assert "Identifier ALM-001-FREEZE" in content
    assert "Version 1.0" in content
    assert "Status Active Freeze" in content


def test_freeze_declares_active_promoted_authority() -> None:
    content = normalized(freeze_text())

    assert "Authority AUTHORITATIVE." in content
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_freeze_declares_exactly_eight_dimensions() -> None:
    content = normalized(freeze_text())

    assert (
        "Exactly eight candidate responsibility dimensions are frozen:"
        in content
    )


def test_freeze_declares_exactly_seven_relationship_types() -> None:
    content = normalized(freeze_text())

    assert (
        "Exactly seven architectural relationship types are frozen:"
        in content
    )


def test_freeze_preserves_multi_dimensional_participation() -> None:
    content = normalized(freeze_text())

    assert "Frozen Multi-Dimensional Participation" in content
    assert (
        "One architectural entity may participate in multiple "
        "responsibility dimensions."
        in content
    )


def test_freeze_preserves_no_relationship_state() -> None:
    content = normalized(freeze_text())

    assert "Frozen No-Relationship State" in content
    assert "No edge shall remain a valid architecture-graph state." in content


def test_freeze_preserves_graph_minimality() -> None:
    content = normalized(freeze_text())

    assert "Frozen Graph Minimality" in content


def test_freeze_preserves_authority_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Authority Boundary" in content
    assert "ALM-001 shall not define normative authority." in content


def test_freeze_preserves_lifecycle_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Lifecycle Boundary" in content


def test_freeze_preserves_processing_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Processing Boundary" in content


def test_freeze_preserves_implementation_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Implementation Boundary" in content


def test_freeze_preserves_observability_disposition() -> None:
    content = normalized(freeze_text())

    assert "Frozen Observability Disposition" in content
    assert "OBSERVABILITY_ARCHITECTURE" in content


def test_freeze_preserves_rejected_placement_identities() -> None:
    content = normalized(freeze_text())

    assert "Frozen Rejected Placement Identities" in content

    for item in (
        "DEPLOYMENT_ARCHITECTURE.",
        "INFRASTRUCTURE_ARCHITECTURE.",
        "TOPOLOGY_ARCHITECTURE.",
    ):
        assert item in content


def test_cycle_1_has_fifty_cases() -> None:
    cases = re.findall(
        r"^# AR-(\d{3}) —",
        text(CYCLE_1),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 51)
    ]


def test_cycle_2_has_forty_cases() -> None:
    cases = re.findall(
        r"^# TR-(\d{3}) —",
        text(CYCLE_2),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 41)
    ]


def test_cycle_3_has_forty_cases() -> None:
    cases = re.findall(
        r"^# PT-(\d{3}) —",
        text(CYCLE_3),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 41)
    ]


def test_cycle_4_has_sixty_cases() -> None:
    cases = re.findall(
        r"^# FM-(\d{3}) —",
        text(CYCLE_4),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 61)
    ]


def test_final_cycle_reports_190_total_adversarial_cases() -> None:
    content = normalized(text(CYCLE_4))

    assert "Total Adversarial Cases 190." in content


def test_final_cycle_reports_zero_taxonomy_expansion() -> None:
    content = normalized(text(CYCLE_4))

    assert "Required Taxonomy Expansion 0." in content


def test_final_cycle_reports_zero_taxonomy_reduction() -> None:
    content = normalized(text(CYCLE_4))

    assert "Required Taxonomy Reduction 0." in content


def test_final_cycle_reports_zero_boundary_leakage_failures() -> None:
    content = normalized(text(CYCLE_4))

    assert "Authority Leakage Failures 0." in content
    assert "Lifecycle Leakage Failures 0." in content
    assert "Processing Leakage Failures 0." in content
    assert "Implementation Leakage Failures 0." in content


def test_final_cycle_declares_freeze_readiness_candidate() -> None:
    content = normalized(text(CYCLE_4))

    assert "Freeze Readiness CANDIDATE." in content
