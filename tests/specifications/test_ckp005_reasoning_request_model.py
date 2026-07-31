"""
Executable Specification

CKP-005.3
Commerce Reasoning Request Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_REASONING_REQUEST_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Request Identity",
    "## Request Version",
    "## Request Lifecycle",
    "## Reasoning Form",
    "## Request Properties",
    "## Goal Assertion Reference",
    "## Graph Target",
    "## Baseline References",
    "## Fact Source References",
    "## Premise References",
    "## Inference Rule References",
    "## Constraint References",
    "## Reasoning Execution Context Reference",
    "## Reasoning Limits",
    "## Closed-World Policy",
    "## Contradiction Policy",
    "## Expected Reasoning Outcome",
    "## Request Evidence",
    "## Request Integrity",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Request Validation",
    "## Validation Result",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Request Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

REASONING_FORMS = (
    "DERIVE ASSERTION.",
    "VALIDATE ASSERTION.",
    "EXPLAIN ASSERTION.",
    "PROVE ASSERTION.",
    "DETECT CONTRADICTION.",
)

EXPECTED_OUTCOMES = (
    "PROVEN.",
    "DISPROVEN.",
    "UNDETERMINED.",
    "CONTRADICTED.",
    "ERROR.",
)

FAILURE_CLASSIFICATIONS = (
    "REQUEST_IDENTITY_VIOLATION.",
    "REQUEST_VERSION_VIOLATION.",
    "REQUEST_LIFECYCLE_VIOLATION.",
    "REASONING_FORM_VIOLATION.",
    "GOAL_REFERENCE_VIOLATION.",
    "GOAL_INTEGRITY_VIOLATION.",
    "GRAPH_TARGET_VIOLATION.",
    "VOCABULARY_BASELINE_VIOLATION.",
    "ONTOLOGY_BASELINE_VIOLATION.",
    "GRAPH_BASELINE_VIOLATION.",
    "QUERY_LANGUAGE_BASELINE_VIOLATION.",
    "FACT_SOURCE_VIOLATION.",
    "PREMISE_REFERENCE_VIOLATION.",
    "RULE_REFERENCE_VIOLATION.",
    "CONSTRAINT_REFERENCE_VIOLATION.",
    "EXECUTION_CONTEXT_VIOLATION.",
    "REASONING_DEPTH_LIMIT_VIOLATION.",
    "RULE_APPLICATION_LIMIT_VIOLATION.",
    "DERIVED_ASSERTION_LIMIT_VIOLATION.",
    "CLOSED_WORLD_POLICY_VIOLATION.",
    "CONTRADICTION_POLICY_VIOLATION.",
    "EXPECTED_OUTCOME_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

REQUEST_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Request Identity.",
    "Request Version Preservation.",
    "Lifecycle Validity.",
    "Canonical Reasoning Form.",
    "Exactly One Goal Assertion.",
    "Immutable Goal Assertion.",
    "Immutable Graph Target.",
    "Vocabulary Baseline Compatibility.",
    "Ontology Baseline Compatibility.",
    "Graph Baseline Compatibility.",
    "Query Language Baseline Compatibility.",
    "Fact Source Closure.",
    "Premise Reference Closure.",
    "Rule Registration Closure.",
    "Constraint Registration Closure.",
    "Execution Context Closure.",
    "Reasoning Depth Boundary.",
    "Rule Application Boundary.",
    "Derived Assertion Boundary.",
    "Explicit Closed-World Policy.",
    "Explicit Contradiction Policy.",
    "Expected Outcome Independence.",
    "Deterministic Fact Source Ordering.",
    "Deterministic Premise Ordering.",
    "Deterministic Rule Ordering.",
    "Deterministic Constraint Ordering.",
    "Canonical Serialization.",
    "Request Evidence Completeness.",
    "Request Integrity.",
    "Fail-Closed Validation.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Request Model" in content
    assert "Abbreviation CRRM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    content = spec_text()

    for section in EXPECTED_SECTIONS:
        assert content.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    content = spec_text()

    positions = [
        content.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-004 Commerce Query Language 1.0.",
        "CKP-005.1 Commerce Reasoning Charter.",
        "CKP-005.2 Commerce Reasoning Structure Model.",
    ):
        assert dependency in content


def test_request_identity_is_immutable_and_unique() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Request shall possess one immutable "
        "Reasoning Request Identifier.",
        "CKP-REASONING-REQUEST-000001",
        "Every Reasoning Request Identifier shall be unique "
        "within one Reasoning Execution Context.",
        "A Reasoning Request Identifier shall never be reused "
        "for a different normative Reasoning Request.",
    ):
        assert requirement in content


def test_request_version_and_lifecycle_are_declared() -> None:
    content = normalized_text()

    assert "The initial supported Reasoning Request Version is: 1.0." in content

    for lifecycle in (
        "Draft.",
        "Approved.",
        "Deprecated.",
        "Retired.",
    ):
        assert lifecycle in content

    assert "Only an Approved Reasoning Request may enter reasoning evaluation." in content


def test_reasoning_forms_are_declared() -> None:
    content = normalized_text()

    for reasoning_form in REASONING_FORMS:
        assert reasoning_form in content

    assert (
        "Every Reasoning Request shall declare exactly one "
        "canonical Reasoning Form."
    ) in content


def test_goal_assertion_reference_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Reasoning Request shall reference exactly one "
        "Goal Assertion."
    ) in content

    for property_name in (
        "Goal Assertion Identifier.",
        "Subject Identifier.",
        "Predicate Identifier.",
        "Object Identifier or Literal Value.",
        "Assertion Polarity.",
        "Assertion Type.",
        "Graph Scope.",
        "Expected Truth Value.",
        "Goal Integrity Reference.",
    ):
        assert property_name in content


def test_graph_and_baseline_targets_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Reasoning Request shall declare one Graph Identifier "
        "and one Graph Version.",
        "Vocabulary Baseline Reference.",
        "Ontology Baseline Reference.",
        "Graph Baseline Reference.",
        "Query Language Baseline Reference.",
        "Baseline references shall be mutually compatible.",
    ):
        assert requirement in content


def test_fact_premise_rule_and_constraint_references_are_declared() -> None:
    content = normalized_text()

    for heading in (
        "Fact Source References",
        "Premise References",
        "Inference Rule References",
        "Constraint References",
    ):
        assert heading in content

    for requirement in (
        "Undocumented Fact Sources shall be invalid.",
        "Duplicate Premise References shall be invalid.",
        "Duplicate Rule References shall be invalid "
        "within one Request scope.",
        "Every mandatory Constraint shall be evaluated.",
    ):
        assert requirement in content


def test_execution_context_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Reasoning Request shall reference exactly one "
        "immutable Reasoning Execution Context."
    ) in content

    assert "Execution Context substitution during evaluation is prohibited." in content


def test_reasoning_limits_are_bounded() -> None:
    content = normalized_text()

    for limit_name in (
        "Maximum Reasoning Depth.",
        "Maximum Rule Applications.",
        "Maximum Derived Assertions.",
    ):
        assert limit_name in content

    for rule in (
        "Every limit shall be a non-negative integer.",
        "Request limits shall not exceed the corresponding "
        "Execution Context limits.",
        "A zero limit shall prohibit the corresponding operation.",
        "A limit violation shall cause fail-closed evaluation.",
    ):
        assert rule in content


def test_closed_world_and_contradiction_policies_are_explicit() -> None:
    content = normalized_text()

    for value in (
        "OPEN WORLD.",
        "EXPLICIT CLOSED WORLD.",
        "REPORT.",
        "FAIL.",
    ):
        assert value in content

    assert "Closed-world behavior shall not be inferred implicitly." in content
    assert (
        "Contradiction Policy shall not delete, rewrite, suppress, "
        "or repair conflicting assertions."
    ) in content


def test_expected_outcomes_are_declared_and_independent() -> None:
    content = normalized_text()

    for outcome in EXPECTED_OUTCOMES:
        assert outcome in content

    for rule in (
        "Expected Reasoning Outcome shall not influence reasoning evaluation.",
        "Actual Reasoning Outcome shall be calculated independently.",
        "UNDETERMINED shall remain distinct from DISPROVEN.",
        "ERROR shall remain distinct from UNDETERMINED.",
    ):
        assert rule in content


def test_request_evidence_and_integrity_are_declared() -> None:
    content = normalized_text()

    assert (
        "Every Reasoning Request shall declare one "
        "Request Evidence Reference."
    ) in content

    assert (
        "Every Reasoning Request shall possess one deterministic "
        "Request Integrity Reference."
    ) in content

    assert (
        "Any normative Request mutation shall invalidate "
        "the Request Integrity Reference."
    ) in content


def test_canonical_serialization_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve Goal Assertion identity.",
        "Preserve Fact Source ordering.",
        "Preserve Premise ordering.",
        "Preserve Rule ordering.",
        "Preserve Constraint ordering.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert rule in content


def test_reference_ordering_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Fact Source Type. Then Fact Source Identifier.",
        "Premise Priority. Then Premise Identifier.",
        "Rule Priority. Then Rule Identifier.",
        "Constraint Priority. Then Constraint Identifier.",
        "Runtime discovery order shall not affect "
        "normative Request ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert rule in content


def test_request_validation_is_fail_closed() -> None:
    content = normalized_text()

    for check in (
        "Reasoning Request Identifier validity.",
        "Reasoning Request Version support.",
        "Lifecycle Status validity.",
        "Reasoning Form validity.",
        "Goal Assertion resolution.",
        "Graph Version compatibility.",
        "Inference Rule registration.",
        "Constraint registration.",
        "Execution Context compatibility.",
        "Request Evidence completeness.",
        "Request Integrity.",
    ):
        assert check in content

    assert "Validation shall fail closed." in content
    assert "An invalid Reasoning Request shall not enter reasoning evaluation." in content


def test_validation_result_is_declared() -> None:
    content = normalized_text()

    assert "Permitted Validation Result values are: PASS. FAIL." in content

    for property_name in (
        "Validation Identifier.",
        "Reasoning Request Identifier.",
        "Validated Request Version.",
        "Validation Outcome.",
        "Detected Violations.",
        "Failure Classifications.",
        "Failure Reasons.",
        "Validation Evidence Reference.",
        "Validation Integrity Reference.",
    ):
        assert property_name in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Reasoning Request Identifier is missing, invalid, "
        "duplicated, or improperly reused.",
        "The Goal Assertion Reference is missing, duplicated, "
        "unresolved, or integrity-invalid.",
        "A baseline reference is missing, unknown, mutable, "
        "incompatible, or unverifiable.",
        "A Request limit exceeds its Execution Context boundary.",
        "Canonical serialization cannot be produced.",
        "Request Evidence cannot be produced.",
        "Request Integrity cannot be established.",
        "The Request attempts to mutate a frozen baseline.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Canonical Commerce Term.",
        "Create an Ontology Assertion.",
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Modify a Graph Component.",
        "Modify a Query Result.",
        "Modify a registered Inference Rule.",
        "Modify a registered Constraint.",
        "Modify an Execution Context.",
        "Modify HAS Foundation 1.0 LTS.",
        "Modify Specification Runtime 1.0.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_request_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in REQUEST_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Request Identity is valid and unique.",
        "Request Version is supported.",
        "Exactly one canonical Reasoning Form is declared.",
        "Exactly one valid Goal Assertion is referenced.",
        "All baseline references are compatible.",
        "All referenced Rules are registered.",
        "Exactly one compatible Execution Context is referenced.",
        "Expected Reasoning Outcome is explicit and independent.",
        "Canonical serialization succeeds.",
        "Request Evidence is complete.",
        "Request Integrity is valid.",
        "No Failure Condition remains open.",
        "The Request does not mutate a frozen baseline.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert "Version 1.0 defines the canonical Reasoning Request contract." in content
    assert "Future implementations shall preserve this normative Request contract." in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.4" in content
    assert "Inference Rule Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]

    assert len(headings) == len(set(headings))
