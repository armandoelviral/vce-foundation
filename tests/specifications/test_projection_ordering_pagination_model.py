from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "PROJECTION_ORDERING_PAGINATION_MODEL.md"
)

FAILURE_CLASSIFICATIONS = (
    "PROJECTION_IDENTITY_VIOLATION.",
    "PROJECTION_PROPERTY_VIOLATION.",
    "PROJECTION_APPLICABILITY_VIOLATION.",
    "PROJECTION_ALIAS_VIOLATION.",
    "PROJECTION_POSITION_VIOLATION.",
    "PROJECTED_RECORD_VIOLATION.",
    "PROJECTION_RESULT_VIOLATION.",
    "ORDERING_IDENTITY_VIOLATION.",
    "ORDERING_PROPERTY_VIOLATION.",
    "ORDERING_APPLICABILITY_VIOLATION.",
    "ORDERING_COMPARABILITY_VIOLATION.",
    "ORDERING_DIRECTION_VIOLATION.",
    "NULL_ORDERING_VIOLATION.",
    "ORDERING_PRIORITY_VIOLATION.",
    "DETERMINISTIC_ORDERING_VIOLATION.",
    "ORDERED_RECORD_SET_VIOLATION.",
    "PAGINATION_IDENTITY_VIOLATION.",
    "LIMIT_VIOLATION.",
    "OFFSET_VIOLATION.",
    "PAGE_BOUNDARY_VIOLATION.",
    "RETURNED_WINDOW_VIOLATION.",
    "RESULT_COUNT_VIOLATION.",
    "ORDERING_PRESERVATION_VIOLATION.",
    "LIFECYCLE_VIOLATION.",
    "BASELINE_VIOLATION.",
    "IMMUTABILITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Projection Identity.",
    "Projection Property Canonicality.",
    "Projection Property Applicability.",
    "Projection Alias Non-Normativity.",
    "Projection Position Integrity.",
    "Projected Record Source Closure.",
    "Projected Record Count Integrity.",
    "Canonical Ordering Identity.",
    "Ordering Property Canonicality.",
    "Ordering Property Applicability.",
    "Ordering Property Comparability.",
    "Ordering Direction Validity.",
    "Explicit Null Ordering.",
    "Deterministic Ordering Priority.",
    "Deterministic Default Ordering.",
    "Deterministic Tie-Breaking.",
    "Ordered Record Set Closure.",
    "Ordered Record Count Integrity.",
    "Canonical Pagination Identity.",
    "Limit Boundary Integrity.",
    "Offset Boundary Integrity.",
    "Page Boundary Integrity.",
    "Matched Record Count Preservation.",
    "Returned Record Count Integrity.",
    "Returned Window Subset Integrity.",
    "Returned Ordering Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Projection Integrity.",
    "Ordering Integrity.",
    "Pagination Integrity.",
    "Canonical Serialization.",
    "Evidence Completeness.",
    "Fail-Closed Validation.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_processing_pipeline_is_defined() -> None:
    content = normalized_text()

    for stage in (
        "Eligible Component Set Resolution.",
        "Projection Expression Resolution.",
        "Projection Validation.",
        "Projection Application.",
        "Projected Record Set Construction.",
        "Ordering Expression Resolution.",
        "Ordering Validation.",
        "Deterministic Ordering Application.",
        "Ordered Record Set Construction.",
        "Pagination Expression Resolution.",
        "Pagination Validation.",
        "Pagination Application.",
        "Returned Result Window Construction.",
        "Evidence Construction.",
        "Integrity Construction.",
    ):
        assert stage in content


def test_projection_expression_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Projection Identifier.",
        "Expression Version.",
        "Query Identifier.",
        "Selection Identifier.",
        "Selected Component Type.",
        "Projected Property References.",
        "Projection Alias References.",
        "Projection Position References.",
        "Projection Integrity Reference.",
        "Projection Validation Evidence Reference.",
    ):
        assert field_name in content


def test_projection_identity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Projection Expression shall possess one "
        "immutable Projection Identifier.",
        "CKP-PROJECTION-000001",
        "Projection Identifiers shall be unique within "
        "one Query Request.",
        "A Projection Identifier shall never be reused "
        "for a different normative Projection Expression.",
    ):
        assert rule in content


def test_projected_properties_are_canonical() -> None:
    content = normalized_text()

    for rule in (
        "Every Projected Property shall be registered.",
        "Every Projected Property shall be applicable "
        "to the selected Graph Component type.",
        "Every Projected Property shall preserve its "
        "canonical normative meaning.",
        "Projection shall not create a canonical property.",
        "Projection shall not modify source Graph Components.",
    ):
        assert rule in content


def test_component_projection_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Canonical Identifier.",
        "Preferred Name.",
        "Knowledge Object Type.",
        "Relationship Identifier.",
        "Source Node Identifier.",
        "Canonical Relationship Type.",
        "Target Node Identifier.",
        "Path Identifier.",
        "Start Node Identifier.",
        "End Node Identifier.",
        "Ordered Node Sequence.",
        "Ordered Edge Sequence.",
        "Path Length.",
    ):
        assert property_name in content


def test_projection_aliases_are_non_normative() -> None:
    content = normalized_text()

    for rule in (
        "Projection Aliases shall not replace canonical "
        "property names.",
        "Projection Aliases shall not change normative "
        "property meaning.",
        "Projection Aliases shall not become canonical identifiers.",
        "Projection Aliases shall not become canonical definitions.",
    ):
        assert rule in content


def test_projection_positions_are_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Projection Position shall be a non-negative integer.",
        "Projection Position values shall be unique "
        "within one Projection Expression.",
        "Lower Projection Position values shall appear "
        "before higher Projection Position values.",
        "Duplicate Projection Position values shall be invalid.",
    ):
        assert rule in content


def test_default_projections_are_declared() -> None:
    content = normalized_text()

    for heading in (
        "Default Graph Node Projection",
        "Default Graph Edge Projection",
        "Default Graph Path Projection",
    ):
        assert heading in content

    assert "Position 0 Canonical Identifier." in content
    assert "Position 0 Relationship Identifier." in content
    assert "Position 0 Path Identifier." in content


def test_projected_records_are_traceable() -> None:
    content = normalized_text()

    for rule in (
        "Every Projected Record shall reference exactly "
        "one source Graph Component.",
        "A Projected Record shall not become an "
        "independent Graph Component.",
        "A Projected Record shall not replace its "
        "source Graph Component.",
        "Every Projected Record shall correspond to "
        "exactly one eligible Graph Component.",
    ):
        assert rule in content


def test_projection_count_integrity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Projected Record Count shall equal Eligible "
        "Component Count before Pagination is applied."
    ) in content


def test_projection_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Applied Property References.",
        "Applied Projection Positions.",
        "Applied Alias References.",
        "Input Component Count.",
        "Projected Record Count.",
        "Property Applicability Result.",
        "Projection Position Validation Result.",
        "Alias Validation Result.",
        "Projection Integrity Result.",
        "Projection Result Integrity Result.",
    ):
        assert field_name in content


def test_ordering_expression_and_identity_are_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Ordering Identifier.",
        "Ordering Property.",
        "Ordering Direction.",
        "Null Ordering.",
        "Ordering Priority.",
        "Ordering Integrity Reference.",
        "Ordering Validation Evidence Reference.",
    ):
        assert field_name in content

    assert "CKP-ORDERING-000001" in content


def test_ordering_properties_are_comparable() -> None:
    content = normalized_text()

    for rule in (
        "Every Ordering Property shall be:",
        "Deterministically comparable.",
        "Unknown, private, inapplicable, or non-comparable "
        "Ordering Properties shall be invalid.",
        "Projection Aliases shall not be used as "
        "normative Ordering Properties.",
    ):
        assert rule in content


def test_comparable_property_types_are_declared() -> None:
    content = normalized_text()

    for value_type in (
        "IDENTIFIER.",
        "TEXT.",
        "INTEGER.",
        "ENUMERATION.",
        "BOOLEAN.",
    ):
        assert value_type in content

    assert (
        "Implicit property type conversion shall be invalid."
        in content
    )


def test_ordering_direction_and_null_ordering_are_defined() -> None:
    content = normalized_text()

    for value in (
        "ASCENDING.",
        "DESCENDING.",
        "NULLS FIRST.",
        "NULLS LAST.",
    ):
        assert value in content

    assert (
        "Implicit platform-specific null ordering shall be prohibited."
        in content
    )


def test_ordering_priority_is_unique() -> None:
    content = normalized_text()

    for rule in (
        "Ordering Priority shall be a non-negative integer.",
        "Ordering Priority values shall be unique "
        "within one Query Request.",
        "Lower Ordering Priority values shall be "
        "applied before higher Ordering Priority values.",
        "Duplicate Ordering Priority values shall be invalid.",
    ):
        assert rule in content


def test_ordering_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Version 1.0 prohibits equal Ordering Priority values.",
        "Graph Node records shall use Canonical Identifier.",
        "Graph Edge records shall use Relationship Identifier.",
        "Graph Path records shall use Path Identifier.",
        "Identical Projected Record Sets and Ordering "
        "Expressions shall produce identical Ordered Record Sets.",
    ):
        assert rule in content


def test_default_ordering_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Graph Node records shall be ordered by "
        "Canonical Identifier in ASCENDING order.",
        "Graph Edge records shall be ordered by "
        "Relationship Identifier in ASCENDING order.",
        "Graph Path records shall be ordered by "
        "Path Identifier in ASCENDING order.",
        "Default ordering shall occur before Pagination Application.",
    ):
        assert rule in content


def test_ordered_record_set_preserves_count() -> None:
    content = normalized_text()

    for rule in (
        "Ordered Record Count shall equal Projected Record Count.",
        "Ordering shall not create or remove Projected Records.",
        "Ordering shall only change record position.",
    ):
        assert rule in content


def test_ordering_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Applied Ordering Identifiers.",
        "Applied Ordering Properties.",
        "Applied Ordering Directions.",
        "Applied Null Ordering Rules.",
        "Applied Ordering Priorities.",
        "Applied Tie-Breaker.",
        "Property Comparability Result.",
        "Priority Validation Result.",
        "Determinism Result.",
    ):
        assert field_name in content


def test_pagination_expression_and_identity_are_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Pagination Identifier.",
        "Ordered Record Set Reference.",
        "Limit.",
        "Offset.",
        "Pagination Integrity Reference.",
        "Pagination Validation Evidence Reference.",
    ):
        assert field_name in content

    assert "CKP-PAGINATION-000001" in content


def test_limit_behavior_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Limit shall be a non-negative integer.",
        "Limit shall not exceed the Maximum Result "
        "Limit declared by Execution Context.",
        "Limit zero shall return an empty Returned Result Window.",
        "Limit zero shall not change Matched Record Count.",
    ):
        assert rule in content


def test_offset_behavior_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Offset shall be a non-negative integer.",
        "Offset zero shall begin at the first Ordered Record.",
        "Offset equal to Ordered Record Count shall "
        "return an empty Returned Result Window.",
        "Offset greater than Ordered Record Count shall "
        "return an empty Returned Result Window.",
        "Offset shall not change Matched Record Count.",
    ):
        assert rule in content


def test_pagination_application_order_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Pagination shall apply Offset first.",
        "Pagination shall apply Limit after Offset.",
        "Pagination shall not reorder records.",
        "Pagination shall not create records.",
        "Pagination affects only the Returned Result Window.",
    ):
        assert rule in content


def test_page_boundary_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Start Position.",
        "End Position Exclusive.",
        "Returned Record Count.",
        "Has Previous Records.",
        "Has Following Records.",
        "Boundary Integrity Reference.",
    ):
        assert field_name in content

    assert (
        "Start Position shall equal the lesser of "
        "Offset and Ordered Record Count."
    ) in content


def test_returned_window_preserves_order_and_origin() -> None:
    content = normalized_text()

    for rule in (
        "Every returned record shall originate from "
        "the referenced Ordered Record Set.",
        "Returned ordering shall preserve Ordered "
        "Record Set ordering.",
        "Matched Record Count shall equal Ordered Record Count.",
    ):
        assert rule in content


def test_pagination_determinism_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Ordered Record Sets.",
        "Page Boundaries.",
        "Returned Result Windows.",
        "Matched Record Counts.",
        "Returned Record Counts.",
        "Offset and Limit values.",
        "Pagination Integrity References.",
    ):
        assert property_name in content


def test_pagination_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Applied Offset.",
        "Applied Limit.",
        "Execution Context Maximum Result Limit.",
        "Boundary Validation Result.",
        "Result Limit Validation Result.",
        "Ordering Preservation Result.",
        "Pagination Integrity Result.",
        "Pagination Result Integrity Result.",
    ):
        assert field_name in content


def test_integrity_models_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Projection Expression shall possess one "
        "deterministic Projection Integrity Reference.",
        "Every Projected Record shall possess one "
        "deterministic Projected Record Integrity Reference.",
        "Every Ordering Expression shall possess one "
        "deterministic Ordering Integrity Reference.",
        "Every Ordered Record Set shall possess one "
        "deterministic Ordered Record Set Integrity Reference.",
        "Every Pagination Expression shall possess one "
        "deterministic Pagination Integrity Reference.",
        "Every Returned Result Window shall possess one "
        "deterministic Returned Window Integrity Reference.",
    ):
        assert rule in content


def test_canonical_serialization_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve Projection Position.",
        "Preserve Ordering Priority.",
        "Preserve Offset and Limit.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert rule in content


def test_validation_models_are_defined() -> None:
    content = normalized_text()

    for heading in (
        "Projection Validation shall verify:",
        "Ordering Validation shall verify:",
        "Pagination Validation shall verify:",
    ):
        assert heading in content

    for validation in (
        "Projected Property applicability.",
        "Projection Position uniqueness.",
        "Ordering Property comparability.",
        "Ordering Priority uniqueness.",
        "Page Boundary correctness.",
        "Matched Record Count preservation.",
        "Ordering preservation.",
    ):
        assert validation in content


def test_validation_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Permitted Validation Result values are: PASS. FAIL.",
        "Validation shall fail closed.",
        "shall not participate in Query execution.",
    ):
        assert rule in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "A Projected Property is unknown or private.",
        "A Projection Position is negative or duplicated.",
        "Projected Record Count differs from Eligible "
        "Component Count before Pagination.",
        "An Ordering Property is unknown, private, "
        "inapplicable, or non-comparable.",
        "Ordering Priority is negative or duplicated.",
        "Deterministic ordering cannot be established.",
        "Limit is negative.",
        "Offset is negative.",
        "Pagination is applied before deterministic ordering.",
        "Matched Record Count is changed by Pagination.",
        "Required evidence cannot be produced.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Modify an Eligible Component Set member.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Projected Property shall be registered and applicable.",
        "Every Projection Position shall be unique.",
        "Every Ordering Property shall be registered, "
        "applicable, and comparable.",
        "Every Ordering Priority shall be unique.",
        "Ordering shall occur before Pagination.",
        "Pagination shall apply Offset before Limit.",
        "Pagination shall preserve Matched Record Count.",
        "Every returned record shall originate from "
        "the Ordered Record Set.",
    ):
        assert constraint in content


def test_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Processing Pipeline is explicitly defined.",
        "Projection Expression and Identity are explicitly defined.",
        "Projected Properties and applicability are "
        "explicitly defined.",
        "Projection Aliases and Positions are explicitly defined.",
        "Projected Record, Projected Record Set, and "
        "Projection Result are explicitly defined.",
        "Ordering Expression and Identity are explicitly defined.",
        "Deterministic and Default Ordering are explicitly defined.",
        "Pagination Expression and Identity are explicitly defined.",
        "Page Boundary is explicitly defined.",
        "Returned Result Window and Pagination Result "
        "are explicitly defined.",
        "Canonical Serialization is explicitly defined.",
        "Read-Only Boundary is declared.",
        "Model Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.7" in content
    assert "Validation Query Model." in content
