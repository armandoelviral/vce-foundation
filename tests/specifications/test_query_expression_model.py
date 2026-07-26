from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "QUERY_EXPRESSION_MODEL.md"
)

EXPRESSION_TYPES = (
    "Selection Expression.",
    "Filter Expression.",
    "Projection Expression.",
    "Ordering Expression.",
    "Pagination Expression.",
    "Validation Expression.",
)

FILTER_PROPERTIES = (
    "Canonical Identifier.",
    "Relationship Identifier.",
    "Path Identifier.",
    "Preferred Name.",
    "Knowledge Object Type.",
    "Canonical Relationship Type.",
    "Source Node Identifier.",
    "Target Node Identifier.",
    "Start Node Identifier.",
    "End Node Identifier.",
    "Directionality.",
    "Lifecycle Status.",
    "Ontology Membership.",
    "Domain Membership.",
    "Path Length.",
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

FAILURE_CLASSIFICATIONS = (
    "EXPRESSION_IDENTITY_VIOLATION.",
    "EXPRESSION_VERSION_VIOLATION.",
    "EXPRESSION_TYPE_VIOLATION.",
    "EXPRESSION_LIFECYCLE_VIOLATION.",
    "QUERY_COMPATIBILITY_VIOLATION.",
    "SELECTION_EXPRESSION_VIOLATION.",
    "FILTER_PROPERTY_VIOLATION.",
    "FILTER_OPERATOR_VIOLATION.",
    "FILTER_VALUE_VIOLATION.",
    "FILTER_GROUP_VIOLATION.",
    "FILTER_PRIORITY_VIOLATION.",
    "PROJECTION_PROPERTY_VIOLATION.",
    "PROJECTION_ORDER_VIOLATION.",
    "ORDERING_PROPERTY_VIOLATION.",
    "ORDERING_PRIORITY_VIOLATION.",
    "PAGINATION_VIOLATION.",
    "VALIDATION_TYPE_VIOLATION.",
    "VALIDATION_SUBJECT_VIOLATION.",
    "VALIDATION_OBJECT_VIOLATION.",
    "VALIDATION_DIRECTION_VIOLATION.",
    "MAXIMUM_DEPTH_VIOLATION.",
    "GRAPH_CLOSURE_VIOLATION.",
    "BASELINE_VIOLATION.",
    "IMMUTABILITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "EXPRESSION_INTEGRITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

EXPRESSION_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Expression Identity.",
    "Expression Version Preservation.",
    "Canonical Expression Type.",
    "Query Reference Closure.",
    "Query Form Compatibility.",
    "Lifecycle Compatibility.",
    "Selection Target Validity.",
    "Filter Property Canonicality.",
    "Filter Operator Validity.",
    "Filter Value Compatibility.",
    "Explicit Filter Conjunction.",
    "Explicit Filter Negation.",
    "Filter Group Closure.",
    "Deterministic Filter Priority.",
    "Projection Property Canonicality.",
    "Projection Order Integrity.",
    "Ordering Property Canonicality.",
    "Deterministic Ordering Priority.",
    "Deterministic Default Ordering.",
    "Pagination Boundary Integrity.",
    "Deterministic Pagination.",
    "Validation Type Validity.",
    "Validation Subject Closure.",
    "Validation Object Closure.",
    "Direction Preservation.",
    "Maximum Depth Enforcement.",
    "Expression Dependency Acyclicity.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Expression Immutability.",
    "Canonical Serialization.",
    "Deterministic Expression Integrity.",
    "Expression Validation Evidence Completeness.",
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


def test_query_expression_model_exists() -> None:
    assert MODEL.is_file()


def test_query_expression_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Expression is one immutable, typed, "
        "and independently validatable component of "
        "a Query Request.",
        "Possess one immutable Expression Identifier.",
        "Declare one canonical Expression Type.",
        "Reference one Query Identifier.",
        "Produce deterministic validation evidence.",
        "Remain immutable during Query execution.",
    ):
        assert rule in content


def test_expression_types_are_declared() -> None:
    content = normalized_text()

    for expression_type in EXPRESSION_TYPES:
        assert expression_type in content

    assert (
        "Unknown or private Expression Types shall be invalid."
        in content
    )


def test_expression_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Expression Identifier.",
        "Expression Version.",
        "Expression Type.",
        "Query Identifier.",
        "Query Form Compatibility.",
        "Lifecycle Status.",
        "Expression Priority.",
        "Expression Integrity Reference.",
        "Validation Evidence Reference.",
        "Source Evidence Reference.",
        "Expression-specific properties.",
    ):
        assert property_name in content


def test_expression_identity_is_defined() -> None:
    content = normalized_text()

    for identifier in (
        "CKP-SELECTION-000001.",
        "CKP-FILTER-000001.",
        "CKP-PROJECTION-000001.",
        "CKP-ORDERING-000001.",
        "CKP-PAGINATION-000001.",
        "CKP-VALIDATION-000001.",
    ):
        assert identifier in content

    assert (
        "Expression Identifiers shall be unique within "
        "one Query Request."
    ) in content

    assert (
        "An Expression Identifier shall never be reused "
        "for a different normative expression."
    ) in content


def test_expression_version_and_lifecycle_are_defined() -> None:
    content = normalized_text()

    assert "Initial Expression Version 1.0" in content

    for status in (
        "Draft.",
        "Approved.",
        "Deprecated.",
        "Retired.",
    ):
        assert status in content

    assert (
        "Retired expressions shall not participate in "
        "Query execution."
    ) in content


def test_selection_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Selection Identifier.",
        "Selection Target.",
        "Query Form.",
        "Selection Scope.",
        "Selection Validation Reference.",
    ):
        assert property_name in content

    for target in (
        "Graph Node.",
        "Graph Edge.",
        "Graph Path.",
    ):
        assert target in content

    assert (
        "Selection shall not create or infer a Graph Component."
        in content
    )


def test_selection_scope_and_compatibility_are_defined() -> None:
    content = normalized_text()

    assert (
        "Selection Scope defines the immutable Graph "
        "boundary within which selection occurs."
    ) in content

    for rule in (
        "SELECT NODE shall select Graph Node.",
        "SELECT EDGE shall select Graph Edge.",
        "SELECT PATH shall select Graph Path.",
        "An incompatible Selection Target and Query Form "
        "shall cause validation failure.",
    ):
        assert rule in content


def test_filter_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in FILTER_PROPERTIES:
        assert property_name in content

    assert (
        "Unknown or private Filter Properties shall be invalid."
        in content
    )


def test_filter_operators_are_declared() -> None:
    content = normalized_text()

    for operator in FILTER_OPERATORS:
        assert operator in content

    assert (
        "Every Filter Operator shall be compatible with "
        "the Filter Property and Filter Value Type."
    ) in content


def test_filter_values_are_typed() -> None:
    content = normalized_text()

    for value_type in (
        "IDENTIFIER.",
        "TEXT.",
        "INTEGER.",
        "BOOLEAN.",
        "ENUMERATION.",
        "IDENTIFIER LIST.",
        "TEXT LIST.",
        "INTEGER LIST.",
    ):
        assert value_type in content

    assert "Implicit type conversion shall be invalid." in content


def test_filter_conjunction_negation_and_groups_are_defined() -> None:
    content = normalized_text()

    for value in (
        "AND.",
        "OR.",
        "NEGATED.",
        "NOT NEGATED.",
    ):
        assert value in content

    assert (
        "Ambiguous Filter grouping shall cause validation failure."
        in content
    )

    assert (
        "Filter Groups shall not contain cyclic references."
        in content
    )


def test_filter_evaluation_order_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Filter Expressions and Filter Groups shall be "
        "evaluated in deterministic priority order.",
        "Lower numeric priority shall be evaluated "
        "before higher numeric priority.",
        "Equal priority values within the same "
        "evaluation scope shall be invalid.",
        "Execution strategy shall not alter normative "
        "filter semantics.",
    ):
        assert rule in content


def test_projection_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Projection Identifier.",
        "Selected Component Type.",
        "Projected Properties.",
        "Projection Aliases.",
        "Projection Order.",
        "Projection Validation Reference.",
    ):
        assert property_name in content

    assert (
        "Projection shall not create a canonical property."
        in content
    )


def test_projection_aliases_and_order_are_non_normative() -> None:
    content = normalized_text()

    for rule in (
        "Projection Aliases are non-normative presentation labels.",
        "A Projection Alias shall not: Replace the "
        "canonical property name.",
        "Every Projected Property shall possess one "
        "unique Projection Position.",
        "Duplicate Projection Positions shall be invalid.",
    ):
        assert rule in content


def test_default_projections_are_declared() -> None:
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
        "Ordered Node Sequence.",
        "Ordered Edge Sequence.",
        "Path Length.",
    ):
        assert property_name in content


def test_ordering_expression_is_defined() -> None:
    content = normalized_text()

    for property_name in (
        "Ordering Identifier.",
        "Ordering Property.",
        "Ordering Direction.",
        "Null Ordering.",
        "Ordering Priority.",
        "Ordering Validation Reference.",
    ):
        assert property_name in content

    for value in (
        "ASCENDING.",
        "DESCENDING.",
        "NULLS FIRST.",
        "NULLS LAST.",
    ):
        assert value in content


def test_ordering_priority_and_defaults_are_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Duplicate Ordering Priority values shall be invalid.",
        "Graph Nodes shall be ordered by Canonical "
        "Identifier in ascending order.",
        "Graph Edges shall be ordered by Relationship "
        "Identifier in ascending order.",
        "Graph Paths shall be ordered by Path Identifier "
        "in ascending order.",
        "Default ordering shall occur before pagination.",
    ):
        assert rule in content


def test_pagination_expression_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request may reference zero or one "
        "Pagination Expression.",
        "Limit and Offset shall be non-negative integers.",
        "Pagination shall occur after filtering, "
        "projection validation, and deterministic ordering.",
        "Pagination shall not alter Matched Record Count.",
        "Pagination shall determine Returned Record Count.",
    ):
        assert rule in content


def test_validation_expression_and_types_are_defined() -> None:
    content = normalized_text()

    for validation_type in (
        "EXISTS.",
        "REACHABLE.",
        "RELATIONSHIP.",
        "PATH.",
    ):
        assert validation_type in content

    assert (
        "A VALIDATE Query Form shall reference exactly "
        "one Validation Expression."
    ) in content


def test_validation_subject_object_and_direction_are_defined() -> None:
    content = normalized_text()

    for direction in (
        "FORWARD.",
        "REVERSE.",
        "BIDIRECTIONAL.",
    ):
        assert direction in content

    for rule in (
        "Every declared Subject Identifier shall resolve "
        "to a registered Graph Component.",
        "Every required Object Identifier shall resolve "
        "to a registered Graph Component.",
        "REVERSE validation shall require a canonical "
        "inverse relationship where applicable.",
    ):
        assert rule in content


def test_maximum_depth_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Maximum Depth shall be a non-negative integer.",
        "Maximum Depth shall not exceed the Maximum "
        "Validation Depth declared by Execution Context.",
        "Maximum Depth zero shall validate only the "
        "Subject Graph Node without traversing an edge.",
    ):
        assert rule in content


def test_expression_composition_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Exactly one Selection Expression.",
        "Zero or more Filter Expressions.",
        "Zero or more Filter Groups.",
        "Zero or one Projection Expression.",
        "Zero or more Ordering Expressions.",
        "Zero or one Pagination Expression.",
        "Every composed expression shall reference the "
        "same Query Identifier.",
    ):
        assert rule in content


def test_expression_dependency_order_is_acyclic() -> None:
    content = normalized_text()

    for stage in (
        "Selection Expression.",
        "Filter Expressions and Filter Groups.",
        "Projection Expression.",
        "Ordering Expressions.",
        "Pagination Expression.",
        "Validation Expression.",
    ):
        assert stage in content

    assert (
        "Circular expression dependencies shall be invalid."
        in content
    )


def test_expression_immutability_and_integrity_are_defined() -> None:
    content = normalized_text()

    assert (
        "Every Query Expression shall become immutable "
        "before Query execution begins."
    ) in content

    assert (
        "Every Query Expression shall possess one "
        "deterministic Expression Integrity Reference."
    ) in content


def test_canonical_serialization_and_equality_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Expression shall possess one "
        "deterministic canonical serialization.",
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Two Query Expressions are normatively equal "
        "when all normative Expression Properties and "
        "expression-specific properties are equal.",
    ):
        assert rule in content


def test_expression_validation_is_defined() -> None:
    content = normalized_text()

    for validation in (
        "Expression Identifier validity.",
        "Expression Version support.",
        "Expression Type validity.",
        "Query Identifier compatibility.",
        "Query Form compatibility.",
        "Property registration.",
        "Operator validity.",
        "Value type compatibility.",
        "Priority uniqueness.",
        "Expression immutability.",
        "Canonical serialization.",
        "Expression Integrity.",
    ):
        assert validation in content


def test_expression_validation_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Permitted Validation Result values are: PASS. FAIL.",
        "Expression validation shall fail closed.",
        "An expression with Validation Result FAIL "
        "shall not participate in Query execution.",
    ):
        assert rule in content


def test_expression_validation_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Evidence Identifier.",
        "Expression Identifier.",
        "Expression Version.",
        "Expression Type.",
        "Query Identifier.",
        "Property Validation Result.",
        "Operator Validation Result.",
        "Value Validation Result.",
        "Grouping Validation Result.",
        "Priority Validation Result.",
        "Graph Closure Result.",
        "Expression Integrity Result.",
        "Validation Result.",
        "Failure Classification.",
        "Failure Reason.",
        "Evidence Integrity Reference.",
    ):
        assert field_name in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Expression Identifier is missing, invalid, "
        "duplicated, or improperly reused.",
        "The Expression Type is unknown or private.",
        "A Filter Property is unknown or inapplicable.",
        "A Filter Operator is unknown or incompatible.",
        "Filter grouping is ambiguous or cyclic.",
        "Ordering Priority is duplicated.",
        "Limit or Offset is negative.",
        "A Validation Subject is unregistered.",
        "Maximum Depth exceeds the Execution Context boundary.",
        "Expression Integrity cannot be established.",
        "Expression Validation Evidence cannot be produced.",
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
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_expression_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Query Expression shall be read-only.",
        "Every Query Expression shall possess one "
        "immutable Expression Identifier.",
        "Every Query Expression shall declare one "
        "canonical Expression Type.",
        "Every Query Expression shall reference one "
        "Query Identifier.",
        "Every expression grouping and priority shall "
        "be explicit and deterministic.",
        "No invalid Query Expression shall participate "
        "in execution.",
    ):
        assert constraint in content


def test_expression_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in EXPRESSION_INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Query Expression is explicitly defined.",
        "Expression Types are explicitly defined.",
        "Expression Properties are explicitly defined.",
        "Expression Identity is explicitly defined.",
        "Selection Expression and Scope are explicitly defined.",
        "Filter Expression, Properties, Operators, and "
        "Values are explicitly defined.",
        "Projection Expression, Aliases, Order, and "
        "Default Projection are explicitly defined.",
        "Pagination Expression and Determinism are "
        "explicitly defined.",
        "Expression Composition and Dependency Order "
        "are explicitly defined.",
        "Expression Validation Evidence is explicitly defined.",
        "Read-Only Boundary is declared.",
        "Query Expression Constraints are declared.",
        "Query Expression Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.5" in content
    assert "Selection and Filter Model." in content
