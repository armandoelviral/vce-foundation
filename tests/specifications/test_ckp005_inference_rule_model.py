"""
Executable Specification

CKP-005.4
Commerce Inference Rule Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_INFERENCE_RULE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Rule Identity",
    "## Rule Version",
    "## Rule Lifecycle",
    "## Rule Type",
    "## Rule Properties",
    "## Preferred Rule Name",
    "## Rule Registry Reference",
    "## Premise Definition",
    "## Premise Conjunction",
    "## Premise Priority",
    "## Variable Definition",
    "## Variable Binding Rules",
    "## Applicability Constraints",
    "## Conclusion Template",
    "## Rule Priority",
    "## Maximum Application Count",
    "## Rule Registration",
    "## Rule Applicability",
    "## Rule Application Input",
    "## Rule Application Result",
    "## Derived Conclusion",
    "## Rule Evidence",
    "## Rule Integrity",
    "## Rule Application Integrity",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Rule Validation",
    "## Validation Result",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Rule Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

RULE_TYPES = (
    "DIRECT.",
    "HIERARCHICAL.",
    "INVERSE.",
    "TRANSITIVE.",
    "COMPOSITIONAL.",
    "CONSTRAINT.",
    "CONTRADICTION.",
)

VARIABLE_TYPES = (
    "GRAPH NODE IDENTIFIER.",
    "GRAPH EDGE IDENTIFIER.",
    "GRAPH PATH IDENTIFIER.",
    "CANONICAL TERM IDENTIFIER.",
    "RELATIONSHIP TYPE.",
    "TEXT.",
    "INTEGER.",
    "BOOLEAN.",
    "ENUMERATION.",
)

APPLICATION_RESULTS = (
    "APPLIED.",
    "NOT APPLICABLE.",
    "FAILED.",
    "CANCELLED.",
)

FAILURE_CLASSIFICATIONS = (
    "RULE_IDENTITY_VIOLATION.",
    "RULE_VERSION_VIOLATION.",
    "RULE_LIFECYCLE_VIOLATION.",
    "RULE_TYPE_VIOLATION.",
    "RULE_REGISTRY_VIOLATION.",
    "PREFERRED_NAME_VIOLATION.",
    "PREMISE_DEFINITION_VIOLATION.",
    "PREMISE_IDENTITY_VIOLATION.",
    "PREMISE_PRIORITY_VIOLATION.",
    "PREMISE_CONJUNCTION_VIOLATION.",
    "VARIABLE_DEFINITION_VIOLATION.",
    "VARIABLE_TYPE_VIOLATION.",
    "VARIABLE_BINDING_VIOLATION.",
    "APPLICABILITY_CONSTRAINT_VIOLATION.",
    "CONCLUSION_TEMPLATE_VIOLATION.",
    "CONCLUSION_VARIABLE_CLOSURE_VIOLATION.",
    "RULE_PRIORITY_VIOLATION.",
    "MAXIMUM_APPLICATION_COUNT_VIOLATION.",
    "RULE_REGISTRATION_VIOLATION.",
    "RULE_APPLICABILITY_VIOLATION.",
    "RULE_APPLICATION_VIOLATION.",
    "CONCLUSION_VIOLATION.",
    "BASELINE_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

RULE_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Rule Identity.",
    "Rule Version Preservation.",
    "Lifecycle Validity.",
    "Canonical Rule Type.",
    "Rule Registration Closure.",
    "Exactly One Rule Registry.",
    "Premise Definition Completeness.",
    "Premise Identity Uniqueness.",
    "Premise Priority Integrity.",
    "Explicit Premise Conjunction.",
    "Variable Definition Completeness.",
    "Variable Type Compatibility.",
    "Variable Binding Completeness.",
    "Variable Binding Consistency.",
    "Applicability Constraint Closure.",
    "Exactly One Conclusion Template.",
    "Conclusion Variable Closure.",
    "Rule Priority Integrity.",
    "Maximum Application Count Enforcement.",
    "Deterministic Premise Ordering.",
    "Deterministic Variable Ordering.",
    "Deterministic Constraint Ordering.",
    "Deterministic Rule Ordering.",
    "Deterministic Rule Application Ordering.",
    "Derived Conclusion Traceability.",
    "Derived Conclusion Non-Registration.",
    "Rule Evidence Completeness.",
    "Rule Integrity.",
    "Rule Application Integrity.",
    "Canonical Serialization.",
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
    assert "Title Commerce Inference Rule Model" in content
    assert "Abbreviation CIRM" in content
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
        "CKP-005.3 Commerce Reasoning Request Model.",
    ):
        assert dependency in content


def test_rule_identity_is_immutable_and_unique() -> None:
    content = normalized_text()

    for requirement in (
        "Every Inference Rule shall possess one immutable "
        "Rule Identifier.",
        "CKP-RULE-000001",
        "Every Rule Identifier shall be globally unique "
        "within one Rule Registry Version.",
        "A Rule Identifier shall never be reused for a "
        "different normative Rule.",
    ):
        assert requirement in content


def test_rule_version_is_declared() -> None:
    content = normalized_text()

    assert "The initial supported Rule Version is: 1.0." in content
    assert "Rule Version shall not replace Rule Identity." in content
    assert (
        "Rule version compatibility shall be verified "
        "before applicability evaluation."
    ) in content


def test_rule_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in (
        "Draft.",
        "Approved.",
        "Deprecated.",
        "Retired.",
    ):
        assert lifecycle in content

    assert "Only an Approved Rule may participate in reasoning." in content
    assert "A Retired Rule shall not participate." in content


def test_rule_types_are_declared() -> None:
    content = normalized_text()

    for rule_type in RULE_TYPES:
        assert rule_type in content

    for rule in (
        "DIRECT derives one Conclusion from explicit "
        "validated Premises.",
        "INVERSE derives only through a registered "
        "canonical inverse relationship.",
        "TRANSITIVE derives only through a Relationship "
        "Type explicitly declared transitive.",
        "Unknown or private Rule Types shall be invalid.",
    ):
        assert rule in content


def test_rule_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Rule Identifier.",
        "Rule Version.",
        "Preferred Rule Name.",
        "Rule Type.",
        "Lifecycle Status.",
        "Rule Registry Reference.",
        "Premise Definitions.",
        "Premise Conjunction.",
        "Variable Definitions.",
        "Variable Binding Rules.",
        "Applicability Constraints.",
        "Conclusion Template.",
        "Rule Priority.",
        "Maximum Application Count.",
        "Rule Evidence Reference.",
        "Rule Integrity Reference.",
        "Source Evidence Reference.",
    ):
        assert property_name in content


def test_preferred_rule_name_is_non_normative() -> None:
    content = normalized_text()

    for rule in (
        "Human-readable.",
        "Stable within one Rule Version.",
        "Non-normative for Rule identity.",
        "Traceable to the Rule Identifier.",
        "A Preferred Rule Name shall not replace the "
        "Rule Identifier.",
    ):
        assert rule in content


def test_rule_registry_reference_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Inference Rule shall reference exactly "
        "one Rule Registry."
    ) in content

    for property_name in (
        "Registry Identifier.",
        "Registry Version.",
        "Registry Status.",
        "Registry Integrity Reference.",
        "Registry Validation Evidence Reference.",
    ):
        assert property_name in content

    assert "An unregistered Rule shall not participate in reasoning." in content


def test_premise_definitions_are_complete() -> None:
    content = normalized_text()

    assert (
        "Every Inference Rule shall declare one or more "
        "Premise Definitions."
    ) in content

    for property_name in (
        "Premise Identifier.",
        "Assertion Pattern.",
        "Required Assertion Type.",
        "Required Polarity.",
        "Required Source Type.",
        "Variable References.",
        "Premise Priority.",
        "Premise Optionality.",
        "Premise Validation Reference.",
        "Premise Integrity Reference.",
    ):
        assert property_name in content

    assert "Duplicate Premise Identifiers shall be invalid." in content


def test_premise_conjunction_is_explicit() -> None:
    content = normalized_text()

    for conjunction in (
        "ALL.",
        "ANY.",
    ):
        assert conjunction in content

    for rule in (
        "Premise Conjunction shall be explicit.",
        "Conjunction shall not be inferred from "
        "presentation order.",
        "Ambiguous Premise grouping shall be invalid.",
    ):
        assert rule in content


def test_premise_priority_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Premise Priority shall be a non-negative integer.",
        "Lower Premise Priority values shall be "
        "evaluated before higher values.",
        "Duplicate Premise Priority values within one "
        "exclusive Premise scope shall be invalid.",
        "Premise Priority shall not change Premise semantics.",
    ):
        assert rule in content


def test_variable_types_are_declared() -> None:
    content = normalized_text()

    for variable_type in VARIABLE_TYPES:
        assert variable_type in content

    assert "Unknown or private Variable Types shall be invalid." in content


def test_variable_binding_rules_are_explicit() -> None:
    content = normalized_text()

    for requirement in (
        "Every referenced Variable shall possess one "
        "explicit Binding Rule.",
        "Every required Variable shall be bound before "
        "Conclusion construction.",
        "Implicit type conversion shall be invalid.",
        "Conflicting Variable Bindings shall invalidate "
        "Rule Applicability.",
        "Variable rebinding within one Rule Application "
        "shall be prohibited.",
    ):
        assert requirement in content


def test_applicability_constraints_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Constraint Identifier.",
        "Constraint Type.",
        "Constraint Scope.",
        "Required Condition.",
        "Forbidden Condition.",
        "Cardinality Condition.",
        "Value Condition.",
        "Graph Scope.",
        "Constraint Priority.",
        "Constraint Integrity Reference.",
        "Constraint Validation Evidence Reference.",
    ):
        assert property_name in content

    assert (
        "Every mandatory Applicability Constraint shall "
        "be satisfied before Rule Application."
    ) in content


def test_conclusion_template_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Inference Rule shall declare exactly one "
        "Conclusion Template."
    ) in content

    for property_name in (
        "Conclusion Template Identifier.",
        "Subject Expression.",
        "Predicate Expression.",
        "Object Expression or Literal Expression.",
        "Assertion Type.",
        "Assertion Polarity.",
        "Conclusion Type.",
        "Graph Scope.",
        "Lifecycle Status.",
        "Conclusion Validation Reference.",
        "Conclusion Integrity Template Reference.",
    ):
        assert property_name in content

    assert (
        "Every required Variable referenced by the "
        "Conclusion Template shall be bound."
    ) in content


def test_rule_priority_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Rule Priority shall be a non-negative integer.",
        "Lower Rule Priority values shall be evaluated "
        "before higher values.",
        "Duplicate Rule Priority values within one "
        "exclusive Rule evaluation scope shall be invalid.",
        "Runtime discovery order shall not replace "
        "normative Rule ordering.",
    ):
        assert rule in content


def test_maximum_application_count_is_enforced() -> None:
    content = normalized_text()

    for rule in (
        "Maximum Application Count shall be a non-negative integer.",
        "A value of zero shall prohibit Rule Application.",
        "A Rule shall not execute after its Maximum "
        "Application Count is reached.",
        "Exceeding Maximum Application Count shall "
        "cause fail-closed evaluation.",
    ):
        assert rule in content


def test_rule_registration_is_fail_closed() -> None:
    content = normalized_text()

    for check in (
        "Rule Identifier uniqueness.",
        "Rule Version support.",
        "Lifecycle validity.",
        "Rule Type validity.",
        "Rule Registry compatibility.",
        "Premise Definition validity.",
        "Variable Definition validity.",
        "Conclusion Template validity.",
        "Canonical serialization.",
        "Rule Evidence completeness.",
        "Rule Integrity.",
    ):
        assert check in content

    assert (
        "A Rule with Registration Result FAIL shall "
        "not participate in reasoning."
    ) in content


def test_rule_applicability_is_explicit() -> None:
    content = normalized_text()

    for condition in (
        "The Rule is registered.",
        "Every mandatory Premise resolves.",
        "Premise polarity is compatible.",
        "Premise conjunction is satisfied.",
        "Every required Variable is bound.",
        "Variable bindings are type-compatible.",
        "Applicability Constraints are satisfied.",
        "Maximum Reasoning Depth is not exceeded.",
        "Maximum Application Count is not exceeded.",
        "Rule Integrity is valid.",
    ):
        assert condition in content

    assert (
        "A Rule shall fail closed when applicability "
        "cannot be established."
    ) in content


def test_rule_application_input_is_immutable() -> None:
    content = normalized_text()

    for property_name in (
        "Rule Application Identifier.",
        "Reasoning Request Identifier.",
        "Resolved Premise References.",
        "Resolved Fact References.",
        "Resolved Derived Assertion References.",
        "Variable Binding Set Reference.",
        "Applicability Constraint Results.",
        "Current Reasoning Depth.",
        "Current Rule Application Count.",
        "Execution Context Reference.",
        "Rule Application Evidence Reference.",
        "Rule Application Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Every Rule Application Input shall remain "
        "immutable during evaluation."
    ) in content


def test_rule_application_results_are_declared() -> None:
    content = normalized_text()

    for result in APPLICATION_RESULTS:
        assert result in content

    for rule in (
        "APPLIED means the Rule produced one valid Conclusion.",
        "NOT APPLICABLE means the Rule was valid but "
        "its applicability conditions were not satisfied.",
        "FAILED means valid evaluation could not be completed.",
        "CANCELLED means evaluation was explicitly "
        "terminated before completion.",
    ):
        assert rule in content


def test_applied_rule_produces_exactly_one_conclusion() -> None:
    content = normalized_text()

    assert (
        "An APPLIED Rule Application shall produce "
        "exactly one Derived Conclusion."
    ) in content

    assert (
        "A Derived Conclusion shall remain distinct "
        "from a registered Fact."
    ) in content

    assert (
        "A Derived Conclusion shall not automatically "
        "enter a frozen baseline."
    ) in content


def test_rule_evidence_is_required_for_every_outcome() -> None:
    content = normalized_text()

    assert (
        "Every registered Rule and every attempted Rule "
        "Application shall produce deterministic evidence."
    ) in content

    assert (
        "No valid, invalid, applicable, non-applicable, "
        "failed, or cancelled Rule evaluation shall "
        "omit evidence."
    ) in content


def test_rule_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Inference Rule shall possess one "
        "deterministic Rule Integrity Reference."
    ) in content

    assert (
        "Any normative Rule mutation shall invalidate "
        "the Rule Integrity Reference."
    ) in content


def test_rule_application_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Rule Application shall possess one "
        "deterministic Rule Application Integrity Reference."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve Premise ordering.",
        "Preserve Premise Conjunction.",
        "Preserve Variable Definitions.",
        "Preserve Variable Binding Rules.",
        "Preserve Applicability Constraint ordering.",
        "Preserve Conclusion Template structure.",
        "Preserve Rule Priority.",
        "Preserve Maximum Application Count.",
        "Preserve Assertion Polarity.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert rule in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Premise Priority. Then Premise Identifier.",
        "Variable Definitions shall be ordered by: "
        "Variable Identifier.",
        "Constraint Priority. Then Constraint Identifier.",
        "Rule Priority. Then Rule Identifier.",
        "Reasoning Depth. Then Rule Priority. Then Rule Identifier. "
        "Then Rule Application Identifier.",
        "Runtime discovery order shall not affect "
        "normative ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert rule in content


def test_rule_validation_is_fail_closed() -> None:
    content = normalized_text()

    for check in (
        "Rule Identifier validity.",
        "Rule Version support.",
        "Lifecycle Status validity.",
        "Rule Type validity.",
        "Rule Registry resolution.",
        "Premise Definition completeness.",
        "Premise Identifier uniqueness.",
        "Variable Type validity.",
        "Variable Binding compatibility.",
        "Conclusion Variable closure.",
        "Maximum Application Count validity.",
        "Rule Evidence completeness.",
        "Rule Integrity.",
    ):
        assert check in content

    assert "Validation shall fail closed." in content
    assert "An invalid Rule shall not be registered or applied." in content


def test_validation_result_is_declared() -> None:
    content = normalized_text()

    assert "Permitted Validation Result values are: PASS. FAIL." in content

    for property_name in (
        "Validation Identifier.",
        "Rule Identifier.",
        "Rule Version.",
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
        "The Rule Identifier is missing, malformed, "
        "duplicated, or improperly reused.",
        "A Premise Identifier is missing or duplicated.",
        "A required Variable cannot be bound.",
        "Conflicting Variable Bindings exist.",
        "A Conclusion Template references an unbound Variable.",
        "Maximum Application Count is exceeded.",
        "Rule Applicability cannot be established.",
        "Canonical serialization cannot be produced.",
        "Rule Evidence cannot be produced.",
        "Rule Integrity cannot be established.",
        "The Rule attempts to mutate source knowledge "
        "or a frozen baseline.",
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
        "Register a Derived Conclusion as a Graph Fact.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Modify a Query Result.",
        "Modify a registered Fact.",
        "Modify a registered Rule during execution.",
        "Modify a registered Constraint.",
        "Modify an Execution Context.",
        "Repair an unresolved Premise.",
        "Repair a missing inverse relationship.",
        "Modify HAS Foundation 1.0 LTS.",
        "Modify Specification Runtime 1.0.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Modify CKP-005.1.",
        "Modify CKP-005.2.",
        "Modify CKP-005.3.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_rule_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in RULE_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Rule Identity is valid and unique.",
        "Rule Version is supported.",
        "Exactly one canonical Rule Type is declared.",
        "Exactly one compatible Rule Registry is referenced.",
        "One or more valid Premise Definitions are declared.",
        "Premise Conjunction is explicit.",
        "Every required Variable Binding Rule is complete.",
        "Exactly one complete Conclusion Template is declared.",
        "Every Conclusion Variable is closed.",
        "Maximum Application Count is valid.",
        "Canonical serialization succeeds.",
        "Rule Evidence is complete.",
        "Rule Integrity is valid.",
        "No Failure Condition remains open.",
        "The Rule does not mutate source knowledge or "
        "a frozen baseline.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Inference Rule contract."
    ) in content

    assert (
        "Future implementations shall preserve this "
        "normative Inference Rule contract."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.5" in content
    assert "Fact and Premise Model." in content


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
