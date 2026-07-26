from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "SELECTION_FILTER_MODEL.md"
)

NODE_FILTER_PROPERTIES = (
    "Canonical Identifier.",
    "Preferred Name.",
    "Knowledge Object Type.",
    "Lifecycle Status.",
    "Ontology Membership.",
    "Domain Membership.",
    "Registry Reference.",
)

EDGE_FILTER_PROPERTIES = (
    "Relationship Identifier.",
    "Source Node Identifier.",
    "Canonical Relationship Type.",
    "Target Node Identifier.",
    "Directionality.",
    "Inverse Relationship Reference.",
    "Lifecycle Status.",
    "Ontology Assertion Reference.",
)

PATH_FILTER_PROPERTIES = (
    "Path Identifier.",
    "Start Node Identifier.",
    "End Node Identifier.",
    "Ordered Node Sequence.",
    "Ordered Edge Sequence.",
    "Traversal Direction.",
    "Path Length.",
    "Validation Result.",
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
    "SELECTION_IDENTITY_VIOLATION.",
    "SELECTION_TARGET_VIOLATION.",
    "SELECTION_SCOPE_VIOLATION.",
    "SELECTION_CARDINALITY_VIOLATION.",
    "CANDIDATE_SET_VIOLATION.",
    "FILTER_IDENTITY_VIOLATION.",
    "FILTER_PROPERTY_VIOLATION.",
    "FILTER_PROPERTY_APPLICABILITY_VIOLATION.",
    "FILTER_OPERATOR_VIOLATION.",
    "FILTER_OPERATOR_COMPATIBILITY_VIOLATION.",
    "FILTER_VALUE_TYPE_VIOLATION.",
    "FILTER_VALUE_COMPATIBILITY_VIOLATION.",
    "FILTER_CONJUNCTION_VIOLATION.",
    "FILTER_NEGATION_VIOLATION.",
    "FILTER_PRIORITY_VIOLATION.",
    "FILTER_GROUP_IDENTITY_VIOLATION.",
    "FILTER_GROUP_CLOSURE_VIOLATION.",
    "FILTER_GROUP_CYCLE_VIOLATION.",
    "FILTER_SET_VIOLATION.",
    "REGISTRY_CLOSURE_VIOLATION.",
    "BASELINE_VIOLATION.",
    "CARDINALITY_VIOLATION.",
    "IMMUTABILITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Selection Identity.",
    "Selection Target Validity.",
    "Query Form Compatibility.",
    "Selection Scope Closure.",
    "Immutable Graph Target.",
    "Candidate Registry Closure.",
    "Deterministic Candidate Ordering.",
    "Selection Cardinality Integrity.",
    "Canonical Filter Identity.",
    "Filter Property Canonicality.",
    "Filter Property Applicability.",
    "Filter Operator Validity.",
    "Filter Operator Compatibility.",
    "Filter Value Type Validity.",
    "Filter Value Compatibility.",
    "Explicit Filter Conjunction.",
    "Explicit Filter Negation.",
    "Filter Group Closure.",
    "Filter Group Acyclicity.",
    "Deterministic Filter Priority.",
    "Deterministic Filter Ordering.",
    "Filter Set Closure.",
    "Eligible Set Subset Integrity.",
    "Eligible Set Ordering Preservation.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Selection Integrity.",
    "Filter Integrity.",
    "Filter Group Integrity.",
    "Filter Set Integrity.",
    "Selection Evidence Completeness.",
    "Filter Validation Evidence Completeness.",
    "Filter Evaluation Evidence Completeness.",
    "Canonical Serialization.",
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


def test_selection_filter_model_exists() -> None:
    assert MODEL.is_file()


def test_pipeline_is_declared() -> None:
    content = normalized_text()

    for stage in (
        "Query Form Validation.",
        "Selection Expression Resolution.",
        "Selection Scope Validation.",
        "Candidate Set Resolution.",
        "Filter Reference Resolution.",
        "Filter Validation.",
        "Filter Group Validation.",
        "Deterministic Filter Ordering.",
        "Filter Evaluation.",
        "Eligible Component Set Construction.",
        "Selection Evidence Construction.",
        "Filter Evidence Construction.",
        "Integrity Construction.",
    ):
        assert stage in content


def test_selection_expression_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Selection Identifier.",
        "Expression Version.",
        "Query Identifier.",
        "Query Form.",
        "Selection Target.",
        "Selection Scope Reference.",
        "Selection Cardinality.",
        "Lifecycle Status.",
        "Selection Integrity Reference.",
        "Selection Validation Evidence Reference.",
        "Source Evidence Reference.",
    ):
        assert field_name in content


def test_selection_identity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Selection Expression shall possess one "
        "immutable Selection Identifier.",
        "CKP-SELECTION-000001",
        "Selection Identifiers shall be unique within "
        "one Query Request.",
        "A Selection Identifier shall never be reused "
        "for a different normative Selection Expression.",
    ):
        assert rule in content


def test_selection_targets_are_declared() -> None:
    content = normalized_text()

    for target in (
        "Graph Node.",
        "Graph Edge.",
        "Graph Path.",
    ):
        assert target in content

    assert (
        "Unknown or private Selection Targets shall be invalid."
        in content
    )


def test_query_form_compatibility_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "SELECT NODE shall select Graph Node.",
        "SELECT EDGE shall select Graph Edge.",
        "SELECT PATH shall select Graph Path.",
        "A Query Form and Selection Target mismatch "
        "shall cause validation failure.",
    ):
        assert rule in content


def test_selection_scope_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Selection Scope Identifier.",
        "Graph Identifier.",
        "Graph Version.",
        "Component Registry Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Execution Context Reference.",
        "Selection Scope Integrity Reference.",
    ):
        assert field_name in content

    assert (
        "Selection shall not escape its declared Selection Scope."
        in content
    )


def test_candidate_set_is_registered_and_ordered() -> None:
    content = normalized_text()

    for rule in (
        "Every candidate Graph Component shall be "
        "registered in the referenced Graph Manifest.",
        "Graph Nodes shall be ordered by Canonical Identifier.",
        "Graph Edges shall be ordered by Relationship Identifier.",
        "Graph Paths shall be ordered by Path Identifier.",
        "No unregistered or implicit Graph Component "
        "may enter the Candidate Set.",
    ):
        assert rule in content


def test_selection_cardinality_is_defined() -> None:
    content = normalized_text()

    for value in (
        "ZERO OR MORE.",
        "ONE OR MORE.",
        "EXACTLY ONE.",
        "ZERO OR ONE.",
    ):
        assert value in content

    assert (
        "Selection Cardinality shall be evaluated after "
        "all Filter Expressions have been applied."
    ) in content


def test_selection_result_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Candidate Count.",
        "Eligible Component Count.",
        "Ordered Eligible Component Identifiers.",
        "Cardinality Validation Result.",
        "Filter Set Reference.",
        "Selection Status.",
        "Failure Classification.",
        "Failure Reason.",
        "Selection Evidence Reference.",
        "Selection Result Integrity Reference.",
    ):
        assert field_name in content


def test_filter_expression_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Filter Identifier.",
        "Expression Version.",
        "Query Identifier.",
        "Selection Identifier.",
        "Filter Property.",
        "Filter Operator.",
        "Filter Value.",
        "Filter Value Type.",
        "Filter Conjunction.",
        "Filter Negation.",
        "Filter Priority.",
        "Filter Group Reference.",
        "Filter Integrity Reference.",
        "Filter Validation Evidence Reference.",
    ):
        assert field_name in content


def test_filter_identity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Filter Expression shall possess one "
        "immutable Filter Identifier.",
        "CKP-FILTER-000001",
        "Filter Identifiers shall be unique within one Query Request.",
        "Duplicate Filter Identifiers shall be invalid.",
    ):
        assert rule in content


def test_filter_property_registry_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        *NODE_FILTER_PROPERTIES,
        *EDGE_FILTER_PROPERTIES,
        *PATH_FILTER_PROPERTIES,
    ):
        assert property_name in content

    assert (
        "A registered property that is inapplicable to "
        "the Selection Target shall be invalid."
    ) in content


def test_identifier_filtering_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Canonical Identifier filtering applies only to Graph Nodes.",
        "Relationship Identifier filtering applies only to Graph Edges.",
        "Path Identifier filtering applies only to Graph Paths.",
    ):
        assert rule in content


def test_name_and_type_filtering_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Preferred Name filtering applies only to Graph Nodes.",
        "Initial Preferred Name comparison shall be "
        "exact and case-sensitive.",
        "Knowledge Object Type filtering applies only to Graph Nodes.",
        "Initial Graph Nodes use: TERM.",
    ):
        assert rule in content


def test_relationship_type_filtering_is_defined() -> None:
    content = normalized_text()

    for relationship_type in (
        "Is A.",
        "Part Of.",
        "Contains.",
        "Tracked As.",
        "Uses.",
        "Used By.",
        "Sold Through.",
        "Applies To.",
    ):
        assert relationship_type in content

    assert (
        "Related To shall not replace a more specific "
        "canonical Relationship Type."
    ) in content


def test_directional_filters_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Source and Target filtering shall preserve "
        "canonical Graph Edge direction.",
        "A Source filter shall not be interpreted as a Target filter.",
        "A Target filter shall not be interpreted as a Source filter.",
        "Start and End filtering shall preserve the "
        "registered direction of the Graph Path.",
    ):
        assert rule in content


def test_lifecycle_ontology_and_domain_filters_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Lifecycle Status filtering applies to Graph Nodes "
        "and Graph Edges.",
        "Filtering shall not infer new Ontology Membership.",
        "Filtering shall not redefine or infer Domain Membership.",
    ):
        assert rule in content


def test_path_length_filtering_is_defined() -> None:
    content = normalized_text()

    assert (
        "Path Length filtering applies only to Graph Paths."
        in content
    )

    assert (
        "Path Length values shall be non-negative integers."
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


def test_operator_semantics_are_defined() -> None:
    content = normalized_text()

    for operator_name in (
        "EQUALS returns true",
        "NOT EQUALS returns true",
        "IN returns true",
        "NOT IN returns true",
        "EXISTS returns true",
        "NOT EXISTS returns true",
    ):
        assert operator_name in content

    assert (
        "Operator semantics shall not depend on storage technology."
        in content
    )


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


def test_filter_conjunction_and_negation_are_explicit() -> None:
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


def test_filter_group_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Filter Group Identifier.",
        "Ordered Filter References.",
        "Ordered Nested Group References.",
        "Group Conjunction.",
        "Group Negation.",
        "Group Priority.",
        "Group Integrity Reference.",
        "Group Validation Evidence Reference.",
    ):
        assert field_name in content


def test_filter_group_closure_is_acyclic() -> None:
    content = normalized_text()

    for rule in (
        "A Filter Group shall not reference itself.",
        "Filter Groups shall not contain direct or "
        "indirect cyclic references.",
        "An orphan Filter Expression or Filter Group "
        "shall not participate in Filter evaluation.",
    ):
        assert rule in content


def test_filter_priority_and_ordering_are_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Lower numeric priority shall be evaluated "
        "before higher numeric priority.",
        "Equal priority values within the same "
        "evaluation scope shall be invalid.",
        "Identical Filter Sets shall produce identical "
        "evaluation order.",
    ):
        assert rule in content


def test_filter_set_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Filter Set Identifier.",
        "Ordered Root Filter References.",
        "Ordered Root Group References.",
        "Filter Count.",
        "Filter Group Count.",
        "Filter Set Integrity Reference.",
        "Filter Set Validation Evidence Reference.",
    ):
        assert field_name in content

    assert (
        "An empty Filter Set shall preserve the entire "
        "Candidate Set as eligible."
    ) in content


def test_filter_evaluation_is_read_only() -> None:
    content = normalized_text()

    for rule in (
        "Preserve Candidate Set ordering.",
        "Apply explicit grouping.",
        "Apply explicit conjunction.",
        "Apply explicit negation.",
        "Respect deterministic priority.",
        "Filter evaluation shall not modify Candidate Set components.",
    ):
        assert rule in content


def test_filter_evaluation_results_are_defined() -> None:
    content = normalized_text()

    for value in (
        "TRUE.",
        "FALSE.",
        "ERROR.",
    ):
        assert value in content

    assert (
        "ERROR shall cause fail-closed Filter Set evaluation."
        in content
    )


def test_eligible_set_is_a_candidate_subset() -> None:
    content = normalized_text()

    for rule in (
        "Every eligible component shall originate from "
        "the Candidate Set.",
        "No Filter evaluation shall create an eligible "
        "component not present in the Candidate Set.",
        "Eligible Component Set ordering shall preserve "
        "Candidate Set canonical order",
    ):
        assert rule in content


def test_selection_and_filter_evidence_are_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Selection Evidence.",
        "Filter Validation Evidence.",
        "Filter Evaluation Evidence.",
        "Evidence Identifier.",
        "Validation Result.",
        "Failure Classification.",
        "Failure Reason.",
        "Evidence Integrity Reference.",
    ):
        assert field_name in content


def test_integrity_models_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Selection Expression shall possess one "
        "deterministic Selection Integrity Reference.",
        "Every Filter Expression shall possess one "
        "deterministic Filter Integrity Reference.",
        "Every Filter Group shall possess one "
        "deterministic Group Integrity Reference.",
    ):
        assert rule in content


def test_canonical_serialization_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve grouping, conjunction, negation, and priority.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert rule in content


def test_validation_models_are_defined() -> None:
    content = normalized_text()

    for validation in (
        "Selection Validation shall verify:",
        "Filter Validation shall verify:",
        "Filter Set Validation shall verify:",
        "Canonical serialization.",
        "Selection Integrity.",
        "Filter Integrity.",
        "Filter Set Integrity.",
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
        "The Selection Target is unknown or private.",
        "The Selection Scope cannot be resolved.",
        "The Candidate Set contains an unregistered or "
        "implicit Graph Component.",
        "The Filter Property is unknown or private.",
        "The Filter Operator is unknown or private.",
        "Filter Priority is duplicated.",
        "A direct or indirect Filter Group cycle exists.",
        "The Filter Set is not closed.",
        "Deterministic Filter ordering cannot be established.",
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
        "Modify a Candidate Set component.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Query Request shall reference exactly "
        "one Selection Expression.",
        "Every Candidate Set component shall be registered.",
        "Every Filter Property shall be canonical and applicable.",
        "Every Filter Conjunction shall be explicit.",
        "Every Filter Negation shall be explicit.",
        "Every Filter Group shall be closed and acyclic.",
        "Every Eligible Component shall originate from "
        "the Candidate Set.",
        "No invalid Filter Expression or Filter Set "
        "shall participate in execution.",
    ):
        assert constraint in content


def test_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Selection and Filter pipeline is explicitly defined.",
        "Selection Expression is explicitly defined.",
        "Selection Scope is explicitly defined.",
        "Candidate Set is explicitly defined.",
        "Filter Expression and Filter Identity are "
        "explicitly defined.",
        "Filter Property Registry is explicitly defined.",
        "Filter Operators and Operator Semantics are "
        "explicitly defined.",
        "Filter Groups, closure, identity, and priority "
        "are explicitly defined.",
        "Filter Set and Filter Evaluation are explicitly defined.",
        "Eligible Component Set is explicitly defined.",
        "Canonical Serialization is explicitly defined.",
        "Read-Only Boundary is declared.",
        "Selection and Filter Constraints are declared.",
        "Selection and Filter Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.6" in content
    assert (
        "Projection, Ordering, and Pagination Model."
        in content
    )
