from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "QUERY_STRUCTURE_MODEL.md"
)

QUERY_COMPONENTS = (
    "Query Manifest.",
    "Query Request.",
    "Query Form.",
    "Selection Expression.",
    "Filter Expression.",
    "Projection Expression.",
    "Ordering Expression.",
    "Pagination Expression.",
    "Validation Expression.",
    "Execution Context.",
    "Query Result.",
    "Query Evidence.",
    "Query Constraint.",
    "Query Integrity Reference.",
)

QUERY_FORMS = (
    "SELECT NODE.",
    "SELECT EDGE.",
    "SELECT PATH.",
    "VALIDATE EXISTS.",
    "VALIDATE REACHABLE.",
    "VALIDATE RELATIONSHIP.",
    "VALIDATE PATH.",
)

FILTER_OPERATORS = (
    "EQUALS.",
    "NOT EQUALS.",
    "IN.",
    "NOT IN.",
    "EXISTS.",
    "NOT EXISTS.",
    "GREATER THAN.",
    "GREATER THAN OR EQUAL.",
    "LESS THAN.",
    "LESS THAN OR EQUAL.",
)

QUERY_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Query Identity.",
    "Query Version Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Selection Target Validity.",
    "Filter Property Canonicality.",
    "Filter Operator Validity.",
    "Filter Value Compatibility.",
    "Projection Property Canonicality.",
    "Ordering Property Canonicality.",
    "Deterministic Ordering.",
    "Deterministic Pagination.",
    "Validation Expression Validity.",
    "Registered Node Closure.",
    "Registered Edge Closure.",
    "Registered Path Closure.",
    "Direction Preservation.",
    "Query Evidence Completeness.",
    "Query Integrity.",
    "Result Integrity.",
    "Deterministic Query Result.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Fail-Closed Evaluation.",
)


def model_text() -> str:
    return MODEL.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        model_text().split()
    )


def test_query_structure_model_exists() -> None:
    assert MODEL.is_file()


def test_query_components_are_declared() -> None:
    content = normalized_text()

    for component in QUERY_COMPONENTS:
        assert component in content


def test_query_manifest_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Query Manifest identifies one complete CQL "
        "Query Request."
    ) in content

    for property_name in (
        "Query Identifier.",
        "Query Version.",
        "Lifecycle Status.",
        "Graph Identifier.",
        "Graph Version.",
        "Query Form.",
        "Selection Expression Reference.",
        "Filter Expression Reference.",
        "Projection Expression Reference.",
        "Ordering Expression Reference.",
        "Pagination Expression Reference.",
        "Validation Expression Reference.",
        "Execution Context Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Query Integrity Reference.",
    ):
        assert property_name in content


def test_query_request_is_read_only() -> None:
    content = normalized_text()

    assert (
        "A Query Request represents one explicit, "
        "read-only request against one immutable "
        "Commerce Knowledge Graph version."
    ) in content

    assert (
        "A Query Request shall not modify its Graph target."
    ) in content


def test_query_identity_is_defined() -> None:
    content = normalized_text()

    assert "CKP-QUERY-000001" in content
    assert "Query Identifiers shall never be reused" in content
    assert (
        "Query identity shall remain distinct from Query Version."
        in content
    )


def test_query_forms_are_declared() -> None:
    content = normalized_text()

    for query_form in QUERY_FORMS:
        assert query_form in content

    assert (
        "Every Query Request shall declare exactly one Query Form."
        in content
    )


def test_selection_expression_is_defined() -> None:
    content = normalized_text()

    for selection_target in (
        "Graph Node.",
        "Graph Edge.",
        "Graph Path.",
    ):
        assert selection_target in content

    assert (
        "Selection shall not create or infer a Graph Component."
        in content
    )


def test_filter_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Filter Identifier.",
        "Filter Property.",
        "Filter Operator.",
        "Filter Value.",
        "Filter Value Type.",
        "Filter Conjunction.",
        "Filter Negation.",
        "Filter Validation Reference.",
    ):
        assert property_name in content

    assert (
        "Every Filter Property shall be registered and canonical."
        in content
    )


def test_filter_operators_are_declared() -> None:
    content = normalized_text()

    for operator in FILTER_OPERATORS:
        assert operator in content

    assert (
        "Unknown or private Filter Operators shall be invalid."
        in content
    )


def test_filter_conjunction_and_negation_are_defined() -> None:
    content = normalized_text()

    for value in (
        "AND.",
        "OR.",
        "NEGATED.",
        "NOT NEGATED.",
    ):
        assert value in content

    assert (
        "Conjunction shall not be inferred from presentation order."
        in content
    )

    assert "Implicit negation shall be invalid." in content


def test_projection_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Projection Identifier.",
        "Projected Properties.",
        "Projection Order.",
        "Projection Validation Reference.",
    ):
        assert property_name in content

    assert (
        "Projection shall not create a canonical property."
        in content
    )


def test_default_projections_are_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Canonical Identifier.",
        "Preferred Name.",
        "Knowledge Object Type.",
        "Relationship Identifier.",
        "Canonical Relationship Type.",
        "Path Identifier.",
        "Ordered Node Sequence.",
        "Ordered Edge Sequence.",
        "Path Length.",
    ):
        assert property_name in content


def test_ordering_expression_is_defined() -> None:
    content = normalized_text()

    for value in (
        "ASCENDING.",
        "DESCENDING.",
        "NULLS FIRST.",
        "NULLS LAST.",
    ):
        assert value in content

    assert (
        "Every Ordering Property shall be registered and comparable."
        in content
    )


def test_default_ordering_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Graph Nodes shall be ordered by Canonical Identifier "
        "in ascending order.",
        "Graph Edges shall be ordered by Relationship Identifier "
        "in ascending order.",
        "Graph Paths shall be ordered by Path Identifier "
        "in ascending order.",
        "Default ordering shall be deterministic.",
    ):
        assert rule in content


def test_pagination_expression_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Limit shall be a non-negative integer.",
        "Offset shall be a non-negative integer.",
        "Pagination shall occur after filtering, projection "
        "validation, and deterministic ordering.",
    ):
        assert rule in content


def test_validation_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Validation Identifier.",
        "Validation Type.",
        "Subject Identifier.",
        "Object Identifier.",
        "Relationship Type.",
        "Direction.",
        "Maximum Depth.",
        "Expected Result.",
        "Validation Evidence Reference.",
    ):
        assert property_name in content


def test_validation_types_are_declared() -> None:
    content = normalized_text()

    for validation_type in (
        "EXISTS.",
        "REACHABLE.",
        "RELATIONSHIP.",
        "PATH.",
    ):
        assert validation_type in content


def test_execution_context_is_immutable() -> None:
    content = normalized_text()

    assert (
        "Execution Context defines the immutable boundary "
        "of one Query execution."
    ) in content

    assert (
        "Execution Context shall remain immutable during "
        "Query execution."
    ) in content


def test_frozen_baselines_are_required() -> None:
    content = normalized_text()

    for baseline in (
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
    ):
        assert baseline in content


def test_query_result_is_defined() -> None:
    content = normalized_text()

    assert (
        "Query Result represents the deterministic terminal "
        "outcome of one Query Request."
    ) in content

    for property_name in (
        "Matched Record Count.",
        "Returned Record Count.",
        "Ordered Results.",
        "Failure Classification.",
        "Failure Reason.",
        "Query Evidence Reference.",
        "Result Integrity Reference.",
    ):
        assert property_name in content


def test_query_status_transitions_are_defined() -> None:
    content = normalized_text()

    for transition in (
        "Not Executed to Running.",
        "Running to Completed.",
        "Running to Failed.",
        "Running to Cancelled.",
    ):
        assert transition in content

    assert (
        "Completed, Failed, and Cancelled are terminal statuses."
        in content
    )


def test_query_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Evidence Identifier.",
        "Applied Filters.",
        "Applied Projection.",
        "Applied Ordering.",
        "Applied Pagination.",
        "Matched Component Identifiers.",
        "Returned Component Identifiers.",
        "Result Hash.",
        "Validation Result.",
        "Failure Classification.",
        "Failure Reason.",
        "Evidence Integrity Reference.",
    ):
        assert field_name in content


def test_query_and_result_integrity_are_defined() -> None:
    content = normalized_text()

    assert (
        "Every Query Request shall possess one deterministic "
        "Query Integrity Reference."
    ) in content

    assert (
        "Every terminal Query Result shall possess one "
        "deterministic Result Integrity Reference."
    ) in content


def test_evaluation_order_is_declared() -> None:
    content = normalized_text()

    for stage in (
        "Query Manifest Validation.",
        "Baseline Validation.",
        "Graph Resolution.",
        "Query Form Validation.",
        "Selection Validation.",
        "Filter Validation.",
        "Filter Evaluation.",
        "Projection Validation.",
        "Ordering Validation.",
        "Deterministic Ordering.",
        "Pagination Validation.",
        "Pagination Application.",
        "Validation Expression Evaluation.",
        "Result Construction.",
        "Evidence Construction.",
        "Integrity Construction.",
        "Terminal Status Validation.",
    ):
        assert stage in content


def test_query_constraints_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall be read-only.",
        "Every Query Request shall reference one immutable "
        "Graph Version.",
        "Every Query Request shall declare one canonical "
        "Query Form.",
        "No Query shall create a Graph Component.",
        "No Query shall modify a Graph Component.",
        "No Query shall create undocumented semantic meaning.",
        "No Query shall redefine a frozen baseline.",
    ):
        assert rule in content


def test_query_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in QUERY_INVARIANTS:
        assert invariant in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Query Manifest is missing.",
        "The Query Form is unknown or private.",
        "A Filter Property is unknown.",
        "A Filter Operator is unknown.",
        "Limit is negative.",
        "Offset is negative.",
        "Query Evidence cannot be produced.",
        "The Query attempts to mutate the Graph.",
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
        "Modify a Graph Node.",
        "Modify a Graph Edge.",
        "Modify a Graph Path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
    ):
        assert prohibition in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Query Components are explicitly defined.",
        "Query Manifest structure is explicitly defined.",
        "Query Request structure is explicitly defined.",
        "Query Forms are explicitly defined.",
        "Filter Expression is explicitly defined.",
        "Projection Expression and Default Projection are "
        "explicitly defined.",
        "Ordering Expression and Default Ordering are "
        "explicitly defined.",
        "Pagination Expression is explicitly defined.",
        "Query Result is explicitly defined.",
        "Query Evidence is explicitly defined.",
        "Deterministic Evaluation Order is explicitly defined.",
        "Read-Only Boundary is declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.3" in content
    assert "Query Request Model." in content
