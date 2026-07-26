from pathlib import Path


MODEL = Path(
    "research/commerce/query_language/"
    "QUERY_REQUEST_MODEL.md"
)

REQUEST_PROPERTIES = (
    "Query Identifier.",
    "Query Version.",
    "Lifecycle Status.",
    "Graph Identifier.",
    "Graph Version.",
    "Query Form.",
    "Selection Expression Reference.",
    "Filter Expression References.",
    "Projection Expression Reference.",
    "Ordering Expression References.",
    "Pagination Expression Reference.",
    "Validation Expression Reference.",
    "Execution Context Reference.",
    "Vocabulary Baseline Reference.",
    "Ontology Baseline Reference.",
    "Graph Baseline Reference.",
    "Query Integrity Reference.",
    "Source Evidence Reference.",
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

FAILURE_CLASSIFICATIONS = (
    "QUERY_IDENTITY_VIOLATION.",
    "QUERY_VERSION_VIOLATION.",
    "LIFECYCLE_VIOLATION.",
    "GRAPH_TARGET_VIOLATION.",
    "QUERY_FORM_VIOLATION.",
    "SELECTION_VIOLATION.",
    "FILTER_VIOLATION.",
    "PROJECTION_VIOLATION.",
    "ORDERING_VIOLATION.",
    "PAGINATION_VIOLATION.",
    "VALIDATION_EXPRESSION_VIOLATION.",
    "EXECUTION_CONTEXT_VIOLATION.",
    "BASELINE_VIOLATION.",
    "COMPLETENESS_VIOLATION.",
    "IMMUTABILITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "QUERY_INTEGRITY_VIOLATION.",
    "EVIDENCE_VIOLATION.",
)

REQUEST_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Query Identity.",
    "Query Version Preservation.",
    "Lifecycle Compatibility.",
    "Immutable Graph Target.",
    "Canonical Query Form.",
    "Query Form Compatibility.",
    "Selection Reference Closure.",
    "Filter Reference Closure.",
    "Projection Reference Closure.",
    "Ordering Reference Closure.",
    "Pagination Reference Closure.",
    "Validation Reference Closure.",
    "Execution Context Closure.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Request Completeness.",
    "Request Immutability.",
    "Canonical Serialization.",
    "Deterministic Query Integrity.",
    "Request Validation Evidence Completeness.",
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


def test_query_request_model_exists() -> None:
    assert MODEL.is_file()


def test_query_request_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall represent exactly "
        "one canonical CQL operation.",
        "Every Query Request shall reference exactly "
        "one immutable Commerce Knowledge Graph version.",
        "Every Query Request shall be read-only.",
        "Every Query Request shall be complete before "
        "execution begins.",
        "A Query Request shall not become a source of "
        "canonical Commerce meaning.",
    ):
        assert rule in content


def test_query_request_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in REQUEST_PROPERTIES:
        assert property_name in content


def test_query_identity_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall possess one "
        "immutable Query Identifier.",
        "CKP-QUERY-000001",
        "Query identity shall remain distinct from "
        "Query Version.",
        "A Query Identifier shall never be reused for "
        "a different normative Query Request.",
    ):
        assert rule in content


def test_query_version_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall declare one Query Version.",
        "Initial Query Version 1.0",
        "Query Version shall not replace Graph Version.",
        "An unsupported Query Version shall cause "
        "validation failure.",
    ):
        assert rule in content


def test_lifecycle_behavior_is_defined() -> None:
    content = normalized_text()

    for status in (
        "Draft.",
        "Approved.",
        "Deprecated.",
        "Retired.",
    ):
        assert status in content

    for rule in (
        "Only Approved Query Requests may enter normal execution.",
        "Retired Query Requests shall not execute.",
    ):
        assert rule in content


def test_graph_target_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "CKP-GRAPH-000001",
        "Initial Graph Version 1.0",
        "The referenced Graph Manifest shall be resolvable.",
        "The Graph Version shall remain immutable during execution.",
        "A Query Request shall not switch Graph Identifier "
        "or Graph Version after execution begins.",
    ):
        assert rule in content


def test_query_forms_are_declared() -> None:
    content = normalized_text()

    for query_form in QUERY_FORMS:
        assert query_form in content

    assert (
        "Every Query Request shall declare exactly one "
        "canonical Query Form."
    ) in content


def test_query_form_compatibility_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "SELECT NODE shall reference a Graph Node "
        "Selection Expression.",
        "SELECT EDGE shall reference a Graph Edge "
        "Selection Expression.",
        "SELECT PATH shall reference a Graph Path "
        "Selection Expression.",
        "VALIDATE EXISTS shall reference one Validation "
        "Expression of type EXISTS.",
        "VALIDATE REACHABLE shall reference one "
        "Validation Expression of type REACHABLE.",
        "VALIDATE RELATIONSHIP shall reference one "
        "Validation Expression of type RELATIONSHIP.",
        "VALIDATE PATH shall reference one Validation "
        "Expression of type PATH.",
    ):
        assert rule in content


def test_selection_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall reference exactly "
        "one Selection Expression.",
        "The Selection Expression shall resolve to one "
        "registered Selection Target.",
        "A missing or unresolved Selection Expression "
        "shall cause validation failure.",
    ):
        assert rule in content


def test_filter_references_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request may reference zero or more "
        "Filter Expressions.",
        "Every referenced Filter Expression shall "
        "possess one unique Filter Identifier.",
        "Duplicate Filter Identifiers shall be prohibited.",
        "Presentation order shall not replace explicit "
        "Filter Conjunction.",
    ):
        assert rule in content


def test_filter_evaluation_order_is_deterministic() -> None:
    content = normalized_text()

    assert (
        "Filter Expressions shall be evaluated in "
        "deterministic Filter Identifier order"
    ) in content

    assert (
        "Evaluation order shall not change the "
        "normative meaning of explicit AND and OR "
        "conjunctions."
    ) in content


def test_projection_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request may reference one Projection Expression.",
        "When Projection Expression is omitted, the "
        "canonical default projection",
        "Projection shall not create or rename canonical properties.",
        "Projection shall not alter source Graph Components.",
    ):
        assert rule in content


def test_ordering_references_are_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request may reference zero or more "
        "Ordering Expressions.",
        "Every Ordering Expression shall possess one "
        "unique Ordering Identifier.",
        "Duplicate Ordering Priority values shall be invalid.",
        "When no Ordering Expression is referenced, "
        "canonical default ordering shall apply.",
    ):
        assert rule in content


def test_pagination_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request may reference one Pagination Expression.",
        "Limit and Offset shall be non-negative integers.",
        "Limit shall not exceed the Maximum Result Limit",
        "Pagination shall apply after filtering and "
        "deterministic ordering.",
        "A Query Request shall not reference more than "
        "one Pagination Expression.",
    ):
        assert rule in content


def test_validation_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A VALIDATE Query Form shall reference exactly "
        "one Validation Expression.",
        "A SELECT Query Form may omit Validation Expression.",
        "Maximum Depth shall not exceed the Maximum "
        "Validation Depth",
        "Validation Expression shall not create semantic inference.",
    ):
        assert rule in content


def test_execution_context_reference_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall reference exactly "
        "one immutable Execution Context.",
        "The Query Request and Execution Context shall "
        "reference the same Graph Identifier and Graph Version.",
    ):
        assert rule in content


def test_frozen_baselines_are_required() -> None:
    content = normalized_text()

    for baseline in (
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
    ):
        assert baseline in content

    assert (
        "An unknown or incompatible baseline shall "
        "cause validation failure."
    ) in content


def test_request_completeness_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Query Request is complete when all "
        "mandatory properties for its Query Form are "
        "present and resolvable."
    ) in content

    assert (
        "An incomplete Query Request shall not enter execution."
    ) in content


def test_request_immutability_is_defined() -> None:
    content = normalized_text()

    assert (
        "A Query Request shall become immutable before "
        "execution begins."
    ) in content

    assert (
        "Any mutation after execution begins shall "
        "invalidate the Query Request."
    ) in content


def test_query_integrity_is_defined() -> None:
    content = normalized_text()

    assert (
        "Every Query Request shall declare one "
        "deterministic Query Integrity Reference."
    ) in content

    for bound_property in (
        "Query Identifier.",
        "Query Version.",
        "Graph Identifier.",
        "Graph Version.",
        "Query Form.",
        "Selection Expression Reference.",
        "Execution Context Reference.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
    ):
        assert bound_property in content


def test_canonical_serialization_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "A Query Request shall possess one deterministic "
        "canonical serialization.",
        "Use deterministic property ordering.",
        "Use deterministic expression reference ordering.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "Query Integrity calculation.",
    ):
        assert rule in content


def test_request_equality_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Two Query Requests are normatively equal when "
        "all normative Query Request Properties are equal.",
        "Non-normative presentation metadata shall not "
        "affect Query Request equality.",
        "Different Query Identifiers shall represent "
        "different Query Requests.",
    ):
        assert rule in content


def test_request_validation_is_defined() -> None:
    content = normalized_text()

    for validation in (
        "Query Identifier validity.",
        "Query Version support.",
        "Lifecycle Status compatibility.",
        "Graph Manifest resolution.",
        "Query Form validity.",
        "Query Form compatibility.",
        "Request completeness.",
        "Request immutability.",
        "Canonical serialization.",
        "Query Integrity.",
    ):
        assert validation in content


def test_validation_result_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Permitted Validation Result values are: PASS. FAIL.",
        "Validation shall fail closed.",
        "A Query Request with Validation Result FAIL "
        "shall not enter execution.",
    ):
        assert rule in content


def test_request_validation_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Evidence Identifier.",
        "Query Identifier.",
        "Graph Resolution Result.",
        "Query Form Validation Result.",
        "Selection Validation Result.",
        "Filter Validation Result.",
        "Projection Validation Result.",
        "Ordering Validation Result.",
        "Pagination Validation Result.",
        "Validation Expression Result.",
        "Execution Context Validation Result.",
        "Baseline Validation Result.",
        "Completeness Validation Result.",
        "Immutability Validation Result.",
        "Canonical Serialization Result.",
        "Query Integrity Result.",
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
        "The Query Identifier is missing or invalid.",
        "The Query Version is missing or unsupported.",
        "The Graph Manifest cannot be resolved.",
        "The Query Form is missing, unknown, or private.",
        "The Selection Expression is missing or unresolved.",
        "A duplicate Filter Identifier exists.",
        "A duplicate Ordering Priority exists.",
        "More than one Pagination Expression is referenced.",
        "The Query Request is incomplete.",
        "Canonical serialization cannot be produced.",
        "Query Integrity cannot be established.",
        "Request Validation Evidence cannot be produced.",
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


def test_query_request_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Query Request shall be read-only.",
        "Every Query Request shall reference exactly "
        "one immutable Graph Version.",
        "Every Query Request shall declare exactly one "
        "canonical Query Form.",
        "Every Query Request shall reference exactly "
        "one Selection Expression.",
        "Every Query Request shall reference exactly "
        "one Execution Context.",
        "Every Query Request shall become immutable "
        "before execution.",
        "No incomplete Query Request shall execute.",
        "No invalid Query Request shall execute.",
    ):
        assert constraint in content


def test_query_request_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in REQUEST_INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Query Request is explicitly defined.",
        "Query Request Properties are explicitly defined.",
        "Query Identity is explicitly defined.",
        "Query Version is explicitly defined.",
        "Graph Target is explicitly defined.",
        "Query Forms and compatibility are explicitly defined.",
        "Request Completeness is explicitly defined.",
        "Request Immutability is explicitly defined.",
        "Query Integrity is explicitly defined.",
        "Canonical Serialization is explicitly defined.",
        "Request Validation is explicitly defined.",
        "Request Validation Evidence is explicitly defined.",
        "Read-Only Boundary is declared.",
        "Query Request Constraints are declared.",
        "Query Request Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.4" in content
    assert "Query Expression Model." in content
