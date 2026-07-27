from pathlib import Path


AUDIT = Path(
    "research/commerce/query_language/"
    "QUERY_CONSISTENCY_AUDIT.md"
)

REQUIRED_AUDITS = (
    "Charter Compatibility Audit.",
    "Query Structure Audit.",
    "Query Request Audit.",
    "Query Expression Audit.",
    "Selection Audit.",
    "Filter Audit.",
    "Projection Audit.",
    "Ordering Audit.",
    "Pagination Audit.",
    "Validation Query Audit.",
    "Initial Executable Query Audit.",
    "Graph Closure Audit.",
    "Baseline Compatibility Audit.",
    "Query Identity Audit.",
    "Expression Identity Audit.",
    "Query Form Audit.",
    "Result Count Audit.",
    "Expected Result Audit.",
    "Evidence Audit.",
    "Integrity Audit.",
    "Determinism Audit.",
    "Read-Only Audit.",
    "Failure Behavior Audit.",
    "Traceability Audit.",
    "Release Eligibility Audit.",
)

FAILURE_CLASSIFICATIONS = (
    "CHARTER_COMPATIBILITY_VIOLATION.",
    "QUERY_STRUCTURE_VIOLATION.",
    "QUERY_REQUEST_VIOLATION.",
    "QUERY_IDENTITY_VIOLATION.",
    "QUERY_FORM_VIOLATION.",
    "QUERY_COUNT_VIOLATION.",
    "EXPRESSION_IDENTITY_VIOLATION.",
    "SELECTION_VIOLATION.",
    "SELECTION_CARDINALITY_VIOLATION.",
    "FILTER_VIOLATION.",
    "FILTER_GROUP_VIOLATION.",
    "PROJECTION_VIOLATION.",
    "ORDERING_VIOLATION.",
    "PAGINATION_VIOLATION.",
    "VALIDATION_QUERY_VIOLATION.",
    "EXISTS_VIOLATION.",
    "RELATIONSHIP_VIOLATION.",
    "REACHABILITY_VIOLATION.",
    "PATH_VIOLATION.",
    "GRAPH_CLOSURE_VIOLATION.",
    "BASELINE_VIOLATION.",
    "EXPECTED_RESULT_VIOLATION.",
    "RESULT_COUNT_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "DETERMINISM_VIOLATION.",
    "READ_ONLY_VIOLATION.",
    "FAILURE_BEHAVIOR_VIOLATION.",
    "TRACEABILITY_VIOLATION.",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Query Identity.",
    "Deterministic Query Ordering.",
    "Query Count Integrity.",
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
    "Projection Source Traceability.",
    "Deterministic Ordering.",
    "Pagination Boundary Integrity.",
    "Matched Record Count Integrity.",
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
    "Graph Registry Closure.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Evidence Completeness.",
    "Evidence Identity Uniqueness.",
    "Result Integrity Completeness.",
    "Result Integrity Uniqueness.",
    "Canonical Serialization.",
    "Deterministic Query Results.",
    "Fail-Closed Validation.",
    "Failure Behavior Integrity.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Non-Mutation.",
)


def audit_text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        audit_text().split()
    )


def test_query_consistency_audit_exists() -> None:
    assert AUDIT.is_file()


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "Commerce Query Language Consistency Audit" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_purpose_is_defined() -> None:
    content = normalized_text()

    assert (
        "Define the normative consistency audit for "
        "Commerce Query Language Version 1.0."
    ) in content

    assert (
        "The audit shall detect violations without "
        "modifying Query Requests, Query Expressions, "
        "Query Results, the Commerce Knowledge Graph, "
        "or any frozen baseline."
    ) in content


def test_audit_target_is_complete() -> None:
    content = normalized_text()

    for target in (
        "CKP-004 Commerce Query Language 1.0.",
        "CKP-004.1 Commerce Query Language Charter.",
        "CKP-004.2 Query Structure Model.",
        "CKP-004.3 Query Request Model.",
        "CKP-004.4 Query Expression Model.",
        "CKP-004.5 Selection and Filter Model.",
        "CKP-004.6 Projection, Ordering, and Pagination Model.",
        "CKP-004.7 Validation Query Model.",
        "CKP-004.8 Initial Executable Queries.",
        "exactly twenty Initial Executable Queries.",
    ):
        assert target in content


def test_frozen_baseline_boundary_is_declared() -> None:
    content = normalized_text()

    for baseline in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-GRAPH-000001.",
        "The target Graph Version is: 1.0.",
    ):
        assert baseline in content


def test_audit_scope_is_complete() -> None:
    content = normalized_text()

    for audit_name in REQUIRED_AUDITS:
        assert audit_name in content


def test_audit_principles_are_declared() -> None:
    content = normalized_text()

    for principle in (
        "Deterministic.",
        "Repeatable.",
        "Read-only.",
        "Non-mutating.",
        "Traceable.",
        "Evidence-producing.",
        "Baseline-aware.",
        "Fail-closed.",
    ):
        assert principle in content


def test_query_structure_order_is_audited() -> None:
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


def test_query_request_requirements_are_audited() -> None:
    content = normalized_text()

    for requirement in (
        "One Query Identifier.",
        "One Query Version.",
        "One Lifecycle Status.",
        "One Graph Identifier.",
        "One Graph Version.",
        "One canonical Query Form.",
        "One Selection Target.",
        "One Execution Context Reference.",
        "One Expected Evidence Reference.",
        "One Expected Result Integrity Reference.",
    ):
        assert requirement in content


def test_query_identity_and_count_are_audited() -> None:
    content = normalized_text()

    assert "exactly twenty Query Identifiers exist." in content
    assert "CKP-QUERY-000001" in content
    assert "CKP-QUERY-000020." in content

    for count in (
        "Initial Executable Query Count 20.",
        "SELECT NODE Query Count 4.",
        "SELECT EDGE Query Count 4.",
        "SELECT PATH Query Count 2.",
        "VALIDATE EXISTS Query Count 2.",
        "VALIDATE RELATIONSHIP Query Count 3.",
        "VALIDATE REACHABLE Query Count 2.",
        "VALIDATE PATH Query Count 3.",
    ):
        assert count in content


def test_query_forms_are_audited() -> None:
    content = normalized_text()

    for query_form in (
        "SELECT NODE.",
        "SELECT EDGE.",
        "SELECT PATH.",
        "VALIDATE EXISTS.",
        "VALIDATE RELATIONSHIP.",
        "VALIDATE REACHABLE.",
        "VALIDATE PATH.",
    ):
        assert query_form in content


def test_selection_and_cardinality_are_audited() -> None:
    content = normalized_text()

    for target in (
        "Graph Node.",
        "Graph Edge.",
        "Graph Path.",
    ):
        assert target in content

    for cardinality in (
        "ZERO OR MORE.",
        "ONE OR MORE.",
        "EXACTLY ONE.",
        "ZERO OR ONE.",
    ):
        assert cardinality in content


def test_filter_semantics_are_audited() -> None:
    content = normalized_text()

    for operator in (
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
    ):
        assert operator in content

    assert "Implicit type conversion shall be invalid." in content


def test_projection_ordering_and_pagination_are_audited() -> None:
    content = normalized_text()

    for rule in (
        "Projection shall not create a canonical property.",
        "Projection aliases shall remain non-normative.",
        "Ordering shall occur before Pagination.",
        "Pagination shall apply Offset before Limit.",
        "Pagination shall preserve Matched Record Count.",
        "Pagination shall not reorder or create records.",
    ):
        assert rule in content


def test_validation_types_and_outcomes_are_audited() -> None:
    content = normalized_text()

    for validation_type in (
        "EXISTS.",
        "RELATIONSHIP.",
        "REACHABLE.",
        "PATH.",
    ):
        assert validation_type in content

    for outcome in (
        "TRUE.",
        "FALSE.",
        "ERROR.",
    ):
        assert outcome in content

    assert (
        "A structurally valid negative proposition "
        "shall return FALSE."
    ) in content

    assert (
        "An unevaluable proposition shall return ERROR."
    ) in content


def test_exists_relationship_reachable_and_path_are_audited() -> None:
    content = normalized_text()

    for rule in (
        "EXISTS shall not require a Validation Object.",
        "RELATIONSHIP shall not evaluate transitive reachability.",
        "A TRUE REACHABLE outcome shall identify one "
        "deterministic continuous witness path.",
        "A FALSE REACHABLE outcome shall not identify "
        "a witness path.",
        "A composed path shall not become a registered "
        "canonical Graph Path through validation.",
        "An implicit Graph Edge shall cause audit failure.",
    ):
        assert rule in content


def test_graph_closure_is_audited() -> None:
    content = normalized_text()

    for requirement in (
        "10 registered Graph Nodes.",
        "12 registered Graph Edges.",
        "4 registered Graph Paths.",
        "CKP-TERM-999999",
        "shall remain unregistered",
    ):
        assert requirement in content


def test_initial_query_results_are_audited() -> None:
    content = normalized_text()

    for result in (
        "IEQ-001 matches ten Graph Nodes.",
        "IEQ-002 matches exactly CKP-TERM-000002.",
        "IEQ-010 returns TRUE for the existence of "
        "CKP-TERM-000002.",
        "IEQ-011 returns FALSE for CKP-TERM-999999.",
        "IEQ-015 returns TRUE with CKP-PATH-000004 as "
        "the witness path.",
        "IEQ-019 returns ERROR for a disconnected "
        "composed path.",
        "IEQ-020 returns CKP-REL-000001 and "
        "CKP-REL-000002.",
    ):
        assert result in content


def test_expected_result_independence_is_audited() -> None:
    content = normalized_text()

    for rule in (
        "Expected Result shall not alter actual graph evaluation.",
        "Expectation Match Result shall be MATCH.",
        "Expectation Match Result shall be MISMATCH.",
        "Expectation Match Result shall be NOT EVALUATED.",
        "Expectation mismatch shall not mutate the "
        "Validation Outcome.",
    ):
        assert rule in content


def test_evidence_and_integrity_are_audited() -> None:
    content = normalized_text()

    assert "CKP-QUERY-EVIDENCE-000001" in content
    assert "CKP-QUERY-EVIDENCE-000020." in content

    assert "CKP-QUERY-RESULT-INTEGRITY-000001" in content
    assert "CKP-QUERY-RESULT-INTEGRITY-000020." in content

    assert "Every evidence reference shall be unique." in content
    assert "Every Result Integrity Reference shall be unique." in content


def test_canonical_serialization_and_determinism_are_audited() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic identifier ordering.",
        "Preserve Filter grouping and priority.",
        "Preserve Projection positions.",
        "Preserve Ordering priority.",
        "Preserve Offset and Limit.",
        "Preserve Validation Direction and Maximum Depth.",
        "Execution Timestamp shall not alter normative "
        "Query Result equality.",
    ):
        assert rule in content


def test_failure_behavior_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Invalid Query Requests shall fail closed.",
        "Invalid Selection Expressions shall fail closed.",
        "Invalid Filter Expressions and Filter Groups "
        "shall fail closed.",
        "Invalid Projection Expressions shall fail closed.",
        "Invalid Ordering Expressions shall fail closed.",
        "Invalid Pagination Expressions shall fail closed.",
        "Invalid Validation Queries shall fail closed.",
        "FALSE shall remain a valid Validation Outcome.",
        "ERROR shall represent an unevaluable proposition.",
    ):
        assert rule in content


def test_read_only_audit_is_declared() -> None:
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
        "Repair a broken relationship.",
        "Repair a disconnected path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_audit_evidence_is_defined() -> None:
    content = normalized_text()

    for field_name in (
        "Evidence Identifier.",
        "Audit Identifier.",
        "CQL Version.",
        "Graph Identifier.",
        "Graph Version.",
        "Audited Query Count.",
        "Expected Result Consistency Result.",
        "Result Count Consistency Result.",
        "Evidence Completeness Result.",
        "Integrity Consistency Result.",
        "Determinism Result.",
        "Read-Only Result.",
        "Traceability Result.",
        "Validation Result.",
        "Failure Classification.",
        "Failure Reason.",
        "Evidence Integrity Reference.",
    ):
        assert field_name in content


def test_audit_result_is_fail_closed() -> None:
    content = normalized_text()

    for rule in (
        "Permitted Audit Result values are: PASS. FAIL.",
        "The audit shall fail closed.",
        "A FAIL result shall make CKP-004 ineligible "
        "for Freeze.",
    ):
        assert rule in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Initial Executable Query Count is not twenty.",
        "A Query Identifier is missing, duplicated, or "
        "out of deterministic order.",
        "Selection Cardinality is violated.",
        "A Filter Group is open, ambiguous, or cyclic.",
        "Pagination is applied before ordering.",
        "FALSE is incorrectly converted into ERROR.",
        "ERROR is incorrectly converted into FALSE.",
        "A composed path is treated as registered.",
        "An implicit Graph Edge is required.",
        "A deliberate unknown identifier is treated as registered.",
        "Audit Evidence cannot be produced.",
    ):
        assert condition in content


def test_non_mutation_is_defined() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Query Request.",
        "Modify a Query Request.",
        "Create or modify a Query Expression.",
        "Create or modify a Query Result.",
        "Create or modify Query Evidence.",
        "Create or modify a Graph Component.",
        "Repair a Query artifact.",
        "Repair a Graph artifact.",
        "Change an expected result to make a test pass.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
    ):
        assert prohibition in content

    assert (
        "The audit shall report violations; it shall "
        "not repair them."
    ) in content


def test_consistency_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_acceptance_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Exactly twenty Query Requests are declared.",
        "All Query Identifiers are unique and "
        "deterministically ordered.",
        "All Query Forms are permitted.",
        "All Ordering is deterministic.",
        "All Pagination boundaries are valid.",
        "All expected counts are consistent.",
        "All Validation Outcomes preserve TRUE, FALSE, "
        "and ERROR semantics.",
        "Read-only behavior is preserved.",
        "Traceability Closure is established.",
        "Audit Evidence is complete.",
        "No mandatory violation remains open.",
    ):
        assert criterion in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Purpose is explicitly defined.",
        "Audit Target is explicitly defined.",
        "Frozen Baseline Boundary is explicitly defined.",
        "Audit Scope is explicitly defined.",
        "Audit Principles are declared.",
        "Query Structure Audit is explicitly defined.",
        "Query Request and Identity Audits are explicitly defined.",
        "Selection and Cardinality Audits are explicitly defined.",
        "Projection Audit is explicitly defined.",
        "Ordering Audit is explicitly defined.",
        "Pagination Audit is explicitly defined.",
        "Validation Query Audit is explicitly defined.",
        "Graph Closure Audit is explicitly defined.",
        "Evidence and Integrity Audits are explicitly defined.",
        "Determinism Audit is explicitly defined.",
        "Read-Only Audit is explicitly defined.",
        "Traceability Audit is explicitly defined.",
        "Audit Result is explicitly defined.",
        "Non-Mutation is explicitly defined.",
        "Consistency Invariants are declared.",
        "Acceptance Criteria are declared.",
        "CKP-004 is eligible for Freeze only when the "
        "Audit Result is PASS.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.10" in content
    assert "Commerce Query Language Freeze." in content
