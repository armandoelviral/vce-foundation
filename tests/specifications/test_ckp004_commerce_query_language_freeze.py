from pathlib import Path


FREEZE = Path(
    "research/commerce/query_language/releases/"
    "CKP004_COMMERCE_QUERY_LANGUAGE_FREEZE_v1.0.0.md"
)

FROZEN_QUERY_FORMS = (
    "SELECT NODE.",
    "SELECT EDGE.",
    "SELECT PATH.",
    "VALIDATE EXISTS.",
    "VALIDATE RELATIONSHIP.",
    "VALIDATE REACHABLE.",
    "VALIDATE PATH.",
)

FROZEN_VALIDATION_TYPES = (
    "EXISTS.",
    "RELATIONSHIP.",
    "REACHABLE.",
    "PATH.",
)

FROZEN_FILTER_OPERATORS = (
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

FREEZE_INVARIANTS = (
    "Foundation Compatibility.",
    "Specification Runtime Compatibility.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Knowledge Graph Compatibility.",
    "Read-Only Preservation.",
    "Canonical Query Identity.",
    "Query Version Preservation.",
    "Canonical Query Form.",
    "Query Form Compatibility.",
    "Selection Target Validity.",
    "Selection Cardinality Integrity.",
    "Filter Property Canonicality.",
    "Filter Operator Compatibility.",
    "Filter Value Compatibility.",
    "Filter Group Closure.",
    "Filter Group Acyclicity.",
    "Projection Property Canonicality.",
    "Projection Alias Non-Normativity.",
    "Deterministic Projection Position.",
    "Deterministic Ordering.",
    "Deterministic Tie-Breaking.",
    "Pagination Boundary Integrity.",
    "Matched Record Count Preservation.",
    "Returned Record Count Integrity.",
    "Canonical Validation Type.",
    "Expected Result Independence.",
    "Validation Outcome Integrity.",
    "Expectation Match Integrity.",
    "Direct Relationship Semantics.",
    "Maximum Depth Enforcement.",
    "Witness Path Continuity.",
    "Deterministic Witness Selection.",
    "Registered Path Closure.",
    "Composed Path Non-Registration.",
    "No Implicit Graph Edges.",
    "Evidence Completeness.",
    "Evidence Identity Uniqueness.",
    "Query Integrity.",
    "Expression Integrity.",
    "Result Integrity.",
    "Canonical Serialization.",
    "Deterministic Query Results.",
    "Fail-Closed Validation.",
    "Failure Behavior Integrity.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Immutable Baseline Preservation.",
)


def freeze_text() -> str:
    return FREEZE.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        freeze_text().split()
    )


def test_freeze_document_exists() -> None:
    assert FREEZE.is_file()


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "Commerce Query Language Freeze" in content
    assert "Version 1.0.0" in content
    assert "Status Frozen" in content
    assert "Release Identifier CKP-004.10" in content
    assert "Language Identifier CQL-1.0" in content


def test_purpose_is_declared() -> None:
    content = normalized_text()

    assert (
        "Declare Commerce Query Language Version 1.0 "
        "as an immutable normative baseline."
    ) in content

    assert (
        "Future Commerce capabilities shall consume "
        "this baseline without modifying its normative "
        "behavior."
    ) in content


def test_freeze_declaration_is_explicit() -> None:
    content = normalized_text()

    for rule in (
        "Commerce Query Language Version 1.0 is hereby "
        "declared Frozen.",
        "CQL 1.0 becomes the normative language baseline",
        "No future capability may redefine CQL 1.0 in-place.",
        "No future capability may silently modify its "
        "query forms, expression semantics, validation "
        "rules, ordering behavior, pagination boundaries, "
        "evidence requirements, or integrity requirements.",
    ):
        assert rule in content


def test_immutable_baseline_contains_all_milestones() -> None:
    content = normalized_text()

    for milestone in (
        "CKP-004.1 Commerce Query Language Charter.",
        "CKP-004.2 Query Structure Model.",
        "CKP-004.3 Query Request Model.",
        "CKP-004.4 Query Expression Model.",
        "CKP-004.5 Selection and Filter Model.",
        "CKP-004.6 Projection, Ordering, and Pagination Model.",
        "CKP-004.7 Validation Query Model.",
        "CKP-004.8 Initial Executable Queries.",
        "CKP-004.9 Query Consistency Audit.",
        "CKP-004.10 Commerce Query Language Freeze.",
    ):
        assert milestone in content

    assert (
        "The complete baseline shall remain immutable."
    ) in content


def test_foundation_boundary_is_preserved() -> None:
    content = normalized_text()

    for baseline in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
    ):
        assert baseline in content

    assert (
        "CQL 1.0 shall not modify their normative "
        "behavior, canonical identities, assertions, "
        "graph structures, relationships, paths, or "
        "integrity references."
    ) in content


def test_frozen_query_forms_are_declared() -> None:
    content = normalized_text()

    for query_form in FROZEN_QUERY_FORMS:
        assert query_form in content

    for rule in (
        "Every CQL 1.0 Query Request shall declare "
        "exactly one frozen Query Form.",
        "Unknown or private Query Forms remain invalid.",
        "No frozen Query Form may be reinterpreted.",
    ):
        assert rule in content


def test_frozen_validation_types_are_declared() -> None:
    content = normalized_text()

    for validation_type in FROZEN_VALIDATION_TYPES:
        assert validation_type in content

    for rule in (
        "TRUE, FALSE, and ERROR semantics shall remain distinct.",
        "Expected Result shall remain independent from "
        "actual Validation Outcome.",
        "MATCH.",
        "MISMATCH.",
        "NOT EVALUATED.",
    ):
        assert rule in content


def test_frozen_filter_operators_are_declared() -> None:
    content = normalized_text()

    for operator in FROZEN_FILTER_OPERATORS:
        assert operator in content

    for rule in (
        "Filter Operator semantics shall remain "
        "technology-independent.",
        "Implicit type conversion shall remain invalid.",
        "Unknown or private Filter Operators shall "
        "remain invalid.",
    ):
        assert rule in content


def test_frozen_ordering_semantics_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "Graph Nodes shall be ordered by Canonical Identifier.",
        "Graph Edges shall be ordered by Relationship Identifier.",
        "Graph Paths shall be ordered by Path Identifier.",
        "Default ordering shall be ascending.",
        "Ordering shall occur before Pagination.",
        "Canonical identifier ordering shall remain the "
        "final deterministic tie-breaker.",
    ):
        assert rule in content


def test_frozen_pagination_semantics_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "Pagination shall apply Offset before Limit.",
        "Limit and Offset shall remain non-negative integers.",
        "Pagination shall occur only after deterministic ordering.",
        "Pagination shall preserve Matched Record Count.",
        "Pagination shall not reorder, create, modify, "
        "or delete records.",
    ):
        assert rule in content


def test_frozen_validation_semantics_are_declared() -> None:
    content = normalized_text()

    for rule in (
        "EXISTS shall validate registration of one Graph Component.",
        "RELATIONSHIP shall validate one direct canonical Graph Edge.",
        "RELATIONSHIP shall not imply transitive reachability.",
        "REACHABLE shall validate traversal under explicit "
        "direction, strategy, and Maximum Depth constraints.",
        "PATH shall validate one registered or explicitly "
        "composed continuous path.",
        "A composed path shall not become a registered "
        "canonical Graph Path through validation.",
    ):
        assert rule in content


def test_initial_executable_query_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "exactly twenty Query Requests.",
        "CKP-QUERY-000001",
        "CKP-QUERY-000020.",
        "CKP-VALIDATION-QUERY-000010",
        "CKP-VALIDATION-QUERY-000019.",
        "The total Initial Executable Query Count is: 20.",
    ):
        assert requirement in content

    for count in (
        "SELECT NODE 4.",
        "SELECT EDGE 4.",
        "SELECT PATH 2.",
        "VALIDATE EXISTS 2.",
        "VALIDATE RELATIONSHIP 3.",
        "VALIDATE REACHABLE 2.",
        "VALIDATE PATH 3.",
    ):
        assert count in content


def test_frozen_graph_target_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Graph Identifier CKP-GRAPH-000001.",
        "Graph Version 1.0.",
        "10 registered Graph Nodes.",
        "12 registered Graph Edges.",
        "4 registered Graph Paths.",
        "CQL 1.0 shall treat this graph as immutable.",
    ):
        assert requirement in content


def test_evidence_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-QUERY-EVIDENCE-000001",
        "CKP-QUERY-EVIDENCE-000020.",
        "No terminal Query Result may omit evidence.",
        "Failure Classification.",
        "Failure Reason.",
        "Result Hash.",
        "Evidence Integrity Reference.",
    ):
        assert requirement in content


def test_integrity_baseline_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Every Query Request shall possess one "
        "deterministic Query Integrity Reference.",
        "Every Query Expression shall possess one "
        "deterministic Expression Integrity Reference.",
        "Every terminal Query Result shall possess one "
        "deterministic Result Integrity Reference.",
        "CKP-QUERY-RESULT-INTEGRITY-000001",
        "CKP-QUERY-RESULT-INTEGRITY-000020.",
    ):
        assert rule in content


def test_determinism_baseline_is_declared() -> None:
    content = normalized_text()

    assert (
        "Identical valid Query Requests executed "
        "against the same immutable Graph Version and "
        "Execution Context shall produce identical "
        "normative terminal results."
    ) in content

    assert (
        "Execution Timestamp shall not alter normative "
        "Query Result equality."
    ) in content


def test_read_only_baseline_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Register a composed Graph Path.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Repair a broken inverse relationship.",
        "Repair a disconnected path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_failure_behavior_is_frozen() -> None:
    content = normalized_text()

    for rule in (
        "CQL 1.0 shall fail closed.",
        "FALSE shall remain a valid Validation Outcome.",
        "ERROR shall represent an unevaluable proposition.",
        "FALSE shall not be converted into ERROR.",
        "ERROR shall not be converted into FALSE.",
        "No failure shall mutate, reinterpret, or repair the Graph.",
    ):
        assert rule in content


def test_compatibility_rules_are_declared() -> None:
    content = normalized_text()

    for compatibility in (
        "Foundation compatibility.",
        "Specification Runtime compatibility.",
        "Vocabulary compatibility.",
        "Ontology compatibility.",
        "Knowledge Graph compatibility.",
        "Query Request compatibility.",
        "Query Expression compatibility.",
        "Query Form compatibility.",
        "Filter semantic compatibility.",
        "Projection compatibility.",
        "Ordering compatibility.",
        "Pagination compatibility.",
        "Validation semantic compatibility.",
        "Evidence compatibility.",
        "Integrity compatibility.",
        "Canonical serialization compatibility.",
        "Deterministic result compatibility.",
        "Read-only compatibility.",
    ):
        assert compatibility in content


def test_allowed_evolution_is_declared() -> None:
    content = normalized_text()

    for capability in (
        "Add new registered Filter Properties.",
        "Add new compatible Filter Operators.",
        "Add new Projection Properties.",
        "Add new comparable Ordering Properties.",
        "Add new optional Query Evidence fields.",
        "Add new compatible Query Forms.",
        "Add new compatible Validation Types.",
        "Add new executable Query specifications.",
        "Add new parser implementations.",
        "Add new interpreter implementations.",
        "Add new storage adapters.",
    ):
        assert capability in content

    assert (
        "Implementation capabilities shall remain "
        "subordinate to the frozen language contract."
    ) in content


def test_forbidden_changes_are_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Changing the meaning of a frozen Query Form.",
        "Changing the meaning of a frozen Validation Type.",
        "Changing Filter Operator semantics.",
        "Changing deterministic Ordering semantics.",
        "Changing Pagination application order.",
        "Changing TRUE, FALSE, or ERROR semantics.",
        "Changing Expected Result independence.",
        "Changing direct RELATIONSHIP semantics.",
        "Treating a composed path as registered.",
        "Allowing undocumented semantic inference.",
        "Removing mandatory evidence.",
        "Removing mandatory integrity references.",
        "Weakening fail-closed validation.",
        "Weakening read-only behavior.",
        "Silently breaking compatibility.",
        "Mutating frozen CQL artifacts in-place.",
    ):
        assert prohibition in content


def test_governance_and_adr_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Architecturally justified.",
        "Explicitly reviewed.",
        "Traceable.",
        "Auditable.",
        "Evidence-producing.",
        "Compatibility-verified.",
        "Regression-verified.",
        "Versioned.",
        "An approved Architecture Decision Record.",
        "Semantic impact analysis.",
        "Compatibility impact analysis.",
        "Migration analysis.",
    ):
        assert requirement in content


def test_regression_requirement_is_declared() -> None:
    content = normalized_text()

    for regression in (
        "HAS Foundation regression.",
        "Specification Runtime regression.",
        "CKP-001 Vocabulary regression.",
        "CKP-002 Ontology regression.",
        "CKP-003 Knowledge Graph regression.",
        "CQL Charter regression.",
        "Query Structure regression.",
        "Query Request regression.",
        "Query Expression regression.",
        "Selection and Filter regression.",
        "Projection, Ordering, and Pagination regression.",
        "Validation Query regression.",
        "Initial Executable Query regression.",
        "Query Consistency Audit regression.",
        "Conformance regression.",
    ):
        assert regression in content

    assert (
        "No modification shall be accepted when any "
        "mandatory regression fails."
    ) in content


def test_versioning_policy_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Semantic Versioning shall govern CQL releases.",
        "Patch releases:",
        "Minor releases:",
        "Major releases:",
        "CQL 1.0 shall remain permanently available",
    ):
        assert rule in content


def test_freeze_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in FREEZE_INVARIANTS:
        assert invariant in content


def test_release_evidence_is_declared() -> None:
    content = normalized_text()

    for evidence in (
        "Successful CKP-004 contract suite.",
        "Successful Query Consistency Audit.",
        "Successful complete regression suite.",
        "Clean working tree.",
        "Exclusive release commit.",
        "Annotated release tag.",
        "Remote tag verification.",
    ):
        assert evidence in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Freeze Declaration is declared.",
        "Immutable Baseline is declared.",
        "Foundation Baseline Boundary is declared.",
        "Frozen Language Components are declared.",
        "Frozen Query Forms are declared.",
        "Frozen Validation Types are declared.",
        "Frozen Filter Operators are declared.",
        "Frozen Ordering Semantics are declared.",
        "Frozen Pagination Semantics are declared.",
        "Frozen Validation Semantics are declared.",
        "Initial Executable Query Baseline is declared.",
        "Frozen Graph Target is declared.",
        "Evidence Baseline is declared.",
        "Integrity Baseline is declared.",
        "Determinism Baseline is declared.",
        "Read-Only Baseline is declared.",
        "Frozen Failure Behavior is declared.",
        "Compatibility Rules are declared.",
        "Allowed Evolution is declared.",
        "Forbidden Changes are declared.",
        "Governance is declared.",
        "ADR Requirement is declared.",
        "Regression Requirement is declared.",
        "Compatibility Verification is declared.",
        "Versioning Policy is declared.",
        "Freeze Invariants are declared.",
        "Release Evidence is declared.",
        "The Query Consistency Audit Result is PASS.",
        "The complete regression suite is successful.",
        "Commerce Query Language Version 1.0 is officially frozen.",
    ):
        assert criterion in content


def test_effectivity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Effective immediately upon successful release "
        "commit and annotated release tag."
    ) in content

    assert (
        "This Freeze remains valid until superseded by "
        "a future major CQL version."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005" in content
    assert "Commerce Reasoning Model." in content
