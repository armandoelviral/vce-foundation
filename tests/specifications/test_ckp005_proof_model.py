"""
Executable Specification

CKP-005.6
Commerce Proof Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_PROOF_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Proof Identity",
    "## Proof Version",
    "## Proof Lifecycle",
    "## Proof Type",
    "## Proof Properties",
    "## Proof Subject",
    "## Proof Outcome Compatibility",
    "## Proof Step Identity",
    "## Proof Step Properties",
    "## Proof Step Position",
    "## Proof Step Input",
    "## Proof Step Output",
    "## Proof Step Dependencies",
    "## Source Fact Closure",
    "## Premise Closure",
    "## Rule Application Closure",
    "## Variable Binding Closure",
    "## Intermediate Conclusion Closure",
    "## Reasoning Depth",
    "## Direct Proof",
    "## Multi-Step Proof",
    "## Negative Proof",
    "## Contradiction Proof",
    "## Constraint Proof",
    "## Proof Construction",
    "## Proof Completeness",
    "## Proof Validation",
    "## Proof Validation Result",
    "## Proof Evidence",
    "## Proof Step Evidence",
    "## Proof Integrity",
    "## Proof Step Integrity",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Proof Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

PROOF_TYPES = (
    "DIRECT PROOF.",
    "MULTI-STEP PROOF.",
    "NEGATIVE PROOF.",
    "CONTRADICTION PROOF.",
    "CONSTRAINT PROOF.",
)

PROOF_LIFECYCLE_VALUES = (
    "Draft.",
    "Constructed.",
    "Validated.",
    "Invalid.",
    "Superseded.",
    "Archived.",
)

FAILURE_CLASSIFICATIONS = (
    "PROOF_IDENTITY_VIOLATION.",
    "PROOF_VERSION_VIOLATION.",
    "PROOF_LIFECYCLE_VIOLATION.",
    "PROOF_TYPE_VIOLATION.",
    "PROOF_SUBJECT_VIOLATION.",
    "OUTCOME_COMPATIBILITY_VIOLATION.",
    "PROOF_STEP_IDENTITY_VIOLATION.",
    "PROOF_STEP_POSITION_VIOLATION.",
    "PROOF_STEP_INPUT_VIOLATION.",
    "PROOF_STEP_OUTPUT_VIOLATION.",
    "PROOF_STEP_DEPENDENCY_VIOLATION.",
    "SOURCE_FACT_CLOSURE_VIOLATION.",
    "PREMISE_CLOSURE_VIOLATION.",
    "RULE_APPLICATION_CLOSURE_VIOLATION.",
    "VARIABLE_BINDING_CLOSURE_VIOLATION.",
    "INTERMEDIATE_CONCLUSION_CLOSURE_VIOLATION.",
    "REASONING_DEPTH_VIOLATION.",
    "DIRECT_PROOF_VIOLATION.",
    "MULTI_STEP_PROOF_VIOLATION.",
    "NEGATIVE_PROOF_VIOLATION.",
    "CONTRADICTION_PROOF_VIOLATION.",
    "CONSTRAINT_PROOF_VIOLATION.",
    "PROOF_COMPLETENESS_VIOLATION.",
    "BASELINE_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "ORDERING_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

PROOF_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Proof Identity.",
    "Proof Version Preservation.",
    "Lifecycle Validity.",
    "Canonical Proof Type.",
    "Exactly One Primary Conclusion.",
    "Reasoning Outcome Compatibility.",
    "Canonical Proof Step Identity.",
    "Proof Step Identity Uniqueness.",
    "Proof Step Position Integrity.",
    "Exactly One Rule Application Per Proof Step.",
    "Proof Step Input Closure.",
    "Proof Step Output Integrity.",
    "Proof Step Dependency Closure.",
    "Proof Step Dependency Acyclicity.",
    "Source Fact Closure.",
    "Premise Closure.",
    "Rule Application Closure.",
    "Variable Binding Closure.",
    "Intermediate Conclusion Closure.",
    "Reasoning Depth Consistency.",
    "Maximum Reasoning Depth Enforcement.",
    "Direct Proof Cardinality.",
    "Multi-Step Proof Continuity.",
    "Explicit Negative Proof Basis.",
    "Contradiction Branch Preservation.",
    "Constraint Reference Closure.",
    "Proof Completeness.",
    "Proof Evidence Completeness.",
    "Proof Step Evidence Completeness.",
    "Proof Integrity.",
    "Proof Step Integrity.",
    "Deterministic Proof Ordering.",
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
    assert "Title Commerce Proof Model" in content
    assert "Abbreviation CPM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    headings = [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]

    for section in EXPECTED_SECTIONS:
        assert headings.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    content = spec_text()

    positions = [
        content.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]

    assert len(headings) == len(set(headings))


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
        "CKP-005.4 Inference Rule Model.",
        "CKP-005.5 Fact and Premise Model.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content


def test_proof_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Proof shall possess exactly one immutable "
        "Proof Identifier.",
        "CKP-PROOF-000001",
        "Every Proof Identifier shall be globally unique "
        "within one Reasoning Execution Context.",
        "A Proof Identifier shall never be reused for a "
        "different normative Proof.",
    ):
        assert requirement in content


def test_proof_version_is_declared() -> None:
    content = normalized_text()

    assert "Every Proof shall declare one Proof Version." in content
    assert "The initial supported Proof Version is: 1.0." in content
    assert "Proof Version shall not replace Proof Identity." in content
    assert (
        "Proof Version compatibility shall be verified "
        "before Proof construction or validation."
    ) in content


def test_proof_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in PROOF_LIFECYCLE_VALUES:
        assert lifecycle in content

    for rule in (
        "A Draft Proof shall not support a terminal "
        "Reasoning Outcome.",
        "Only a Validated Proof may support PROVEN, "
        "DISPROVEN, or CONTRADICTED.",
        "An Invalid Proof shall not support a normative Conclusion.",
        "Lifecycle Status shall not regress.",
    ):
        assert rule in content


def test_proof_types_are_declared() -> None:
    content = normalized_text()

    for proof_type in PROOF_TYPES:
        assert proof_type in content

    for rule in (
        "DIRECT PROOF contains one valid Proof Step.",
        "MULTI-STEP PROOF contains two or more "
        "dependency-ordered Proof Steps.",
        "NEGATIVE PROOF supports one explicit negative Conclusion.",
        "CONTRADICTION PROOF preserves valid proofs for "
        "both one Assertion and its explicit negation.",
        "Unknown or private Proof Types shall be invalid.",
    ):
        assert rule in content


def test_proof_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Proof Identifier.",
        "Proof Version.",
        "Proof Type.",
        "Lifecycle Status.",
        "Reasoning Request Identifier.",
        "Goal Assertion Identifier.",
        "Conclusion Identifier.",
        "Reasoning Outcome.",
        "Graph Identifier.",
        "Graph Version.",
        "Execution Context Reference.",
        "Source Fact References.",
        "Premise References.",
        "Rule Application References.",
        "Variable Binding References.",
        "Intermediate Conclusion References.",
        "Ordered Proof Step References.",
        "Contradiction Proof References.",
        "Maximum Reasoning Depth.",
        "Actual Reasoning Depth.",
        "Proof Evidence Reference.",
        "Proof Validation Reference.",
        "Proof Integrity Reference.",
        "Source Evidence Reference.",
    ):
        assert property_name in content


def test_proof_subject_is_exactly_one_conclusion() -> None:
    content = normalized_text()

    assert "Every Proof shall support exactly one primary Conclusion." in content

    for rule in (
        "The primary Conclusion shall resolve to one "
        "valid Derived Conclusion or validated Assertion.",
        "A Proof shall not replace, rewrite, or repair "
        "its supported Conclusion.",
    ):
        assert rule in content


def test_proof_outcome_compatibility_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "PROVEN shall require one valid positive Proof.",
        "DISPROVEN shall require one valid Proof "
        "supporting the explicit negation of the Goal.",
        "UNDETERMINED shall not possess a Proof claiming "
        "the Goal or its negation is established.",
        "CONTRADICTED shall require valid Proofs for "
        "both the Goal and its explicit negation.",
        "ERROR shall not be represented as a valid logical Proof.",
        "A Proof shall not alter the actual Reasoning Outcome.",
    ):
        assert rule in content


def test_proof_step_identity_is_unique() -> None:
    content = normalized_text()

    for requirement in (
        "Every Proof Step shall possess exactly one "
        "immutable Proof Step Identifier.",
        "CKP-PROOF-STEP-000001",
        "Every Proof Step Identifier shall be unique within one Proof.",
        "Proof Step identity shall remain distinct from "
        "Proof Step Position.",
    ):
        assert requirement in content


def test_proof_step_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Proof Step Identifier.",
        "Proof Identifier.",
        "Proof Step Position.",
        "Rule Application Identifier.",
        "Rule Identifier.",
        "Rule Version.",
        "Input Assertion References.",
        "Source Fact References.",
        "Premise References.",
        "Variable Bindings.",
        "Dependency Proof Step References.",
        "Produced Conclusion Reference.",
        "Step Reasoning Depth.",
        "Step Validation Result.",
        "Step Evidence Reference.",
        "Step Integrity Reference.",
    ):
        assert property_name in content

    assert "A Proof Step shall reference exactly one Rule Application." in content


def test_proof_step_position_is_deterministic() -> None:
    content = normalized_text()

    for rule in (
        "Proof Step Position shall be a non-negative integer.",
        "Proof Step Positions shall be unique within one Proof.",
        "Proof Step Position shall define deterministic "
        "Proof presentation order.",
        "A Proof Step shall not depend on a later Proof Step.",
    ):
        assert rule in content


def test_proof_step_inputs_are_explicit() -> None:
    content = normalized_text()

    for input_type in (
        "Validated Facts.",
        "Satisfied Premises.",
        "Validated Derived Assertions.",
        "Validated Constraint Results.",
        "Registered Rule References.",
        "Resolved Variable Bindings.",
    ):
        assert input_type in content

    for rule in (
        "Every input reference shall resolve.",
        "Every input shall be integrity-valid.",
        "An undocumented or implicit input shall cause "
        "validation failure.",
    ):
        assert rule in content


def test_proof_step_output_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Proof Step shall produce exactly one "
        "Conclusion Reference."
    ) in content

    for rule in (
        "The Conclusion shall match the associated Rule "
        "Application Result.",
        "The Conclusion shall conform to the Rule "
        "Conclusion Template.",
        "A Proof Step shall not directly register its "
        "Conclusion as a Graph Fact.",
        "A Proof Step shall not modify any input artifact.",
    ):
        assert rule in content


def test_proof_step_dependencies_are_acyclic() -> None:
    content = normalized_text()

    for rule in (
        "Every dependency shall be explicit.",
        "Every dependency reference shall resolve "
        "within the same Proof.",
        "Dependency graphs shall be acyclic.",
        "A Proof Step shall not depend on itself.",
        "Circular Proof Step dependencies shall cause "
        "validation failure.",
        "Orphan intermediate Conclusions shall cause "
        "validation failure.",
    ):
        assert rule in content


def test_source_fact_closure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every source Fact required by a Proof shall be "
        "explicitly referenced.",
        "Approved.",
        "Version-compatible.",
        "Integrity-valid.",
        "Evidence-complete.",
        "Graph-compatible.",
        "Baseline-compatible.",
        "No Proof shall depend on an undocumented Fact.",
    ):
        assert requirement in content


def test_premise_closure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Premise consumed by a Proof Step shall be "
        "explicitly referenced.",
        "Every mandatory Premise shall be satisfied.",
        "Premise polarity shall remain compatible with "
        "the Rule definition.",
        "An unresolved or unsatisfied mandatory Premise "
        "shall invalidate the affected Proof Step and Proof.",
    ):
        assert requirement in content


def test_rule_application_closure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Proof Step shall reference one valid Rule Application.",
        "Every Rule Application shall reference one "
        "registered Inference Rule.",
        "Rule Application Result shall be APPLIED.",
        "Rule Application Integrity shall be valid.",
        "A failed, cancelled, or non-applicable Rule "
        "Application shall not produce a valid Proof Step.",
    ):
        assert requirement in content


def test_variable_binding_closure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Complete.",
        "Type-compatible.",
        "Scope-compatible.",
        "Cardinality-compatible.",
        "Traceable to its binding source.",
        "Integrity-valid.",
        "Conflicting, missing, implicit, or out-of-scope "
        "Variable Bindings shall invalidate the Proof Step.",
    ):
        assert requirement in content


def test_intermediate_conclusion_closure_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every intermediate Conclusion used by a later "
        "Proof Step shall be produced by an earlier "
        "Proof Step within the same Proof.",
        "Producing Proof Step Reference.",
        "Producing Rule Application Reference.",
        "Every intermediate Conclusion shall remain "
        "traceable to source Facts.",
        "Unsupported or orphan intermediate Conclusions "
        "shall invalidate the Proof.",
    ):
        assert requirement in content


def test_reasoning_depth_is_consistent() -> None:
    content = normalized_text()

    for rule in (
        "Source Facts have Reasoning Depth zero.",
        "A Conclusion produced directly from source "
        "Facts has Reasoning Depth one.",
        "Actual Reasoning Depth shall equal the maximum "
        "Proof Step Reasoning Depth.",
        "Actual Reasoning Depth shall not exceed Maximum "
        "Reasoning Depth.",
        "An inconsistent or exceeded Reasoning Depth "
        "shall invalidate the Proof.",
    ):
        assert rule in content


def test_direct_proof_cardinality_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "A DIRECT PROOF shall contain exactly one Proof Step.",
        "The Proof Step shall produce the primary Conclusion.",
        "A DIRECT PROOF shall not contain an intermediate "
        "Conclusion dependency.",
        "A DIRECT PROOF with zero or multiple Proof Steps "
        "shall be invalid.",
    ):
        assert rule in content


def test_multi_step_proof_continuity_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "A MULTI-STEP PROOF shall contain two or more Proof Steps.",
        "Every dependency shall be explicit and acyclic.",
        "The final Proof Step shall produce the primary Conclusion.",
        "A truncated or discontinuous MULTI-STEP PROOF "
        "shall be invalid.",
    ):
        assert rule in content


def test_negative_proof_requires_explicit_basis() -> None:
    content = normalized_text()

    for rule in (
        "A NEGATIVE PROOF shall support one explicit "
        "negative Conclusion.",
        "Absence of positive evidence shall not by "
        "itself establish a NEGATIVE PROOF under OPEN WORLD.",
        "A NEGATIVE PROOF shall preserve Assertion Polarity.",
    ):
        assert rule in content


def test_contradiction_proof_preserves_both_branches() -> None:
    content = normalized_text()

    for rule in (
        "A CONTRADICTION PROOF shall preserve two "
        "independently valid Proof branches.",
        "Both Proof branches shall remain independently verifiable.",
        "Neither branch shall be deleted, suppressed, "
        "rewritten, or prioritized as a repair action.",
    ):
        assert rule in content


def test_constraint_proof_is_declared() -> None:
    content = normalized_text()

    assert (
        "A CONSTRAINT PROOF shall reference exactly one "
        "registered Constraint."
    ) in content

    for property_name in (
        "Constraint Identifier.",
        "Constraint Version.",
        "Constraint Type.",
        "Required Assertions.",
        "Forbidden Assertions.",
        "Cardinality Results.",
        "Value Results.",
        "Constraint Outcome.",
        "Constraint Evidence Reference.",
        "Constraint Integrity Reference.",
    ):
        assert property_name in content


def test_proof_construction_is_fail_closed() -> None:
    content = normalized_text()

    for prerequisite in (
        "Reasoning Request validation.",
        "Goal Assertion validation.",
        "Fact validation.",
        "Premise validation.",
        "Rule registration validation.",
        "Rule applicability validation.",
        "Rule Application completion.",
        "Variable Binding validation.",
        "Conclusion validation.",
    ):
        assert prerequisite in content

    assert (
        "Proof Construction shall fail closed when "
        "Proof completeness cannot be established."
    ) in content


def test_proof_completeness_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "The Proof Identifier is valid.",
        "The Proof Version is supported.",
        "The primary Conclusion resolves.",
        "Every source Fact resolves.",
        "Every mandatory Premise resolves and is satisfied.",
        "Every Rule Application resolves and is valid.",
        "Every Proof Step dependency resolves.",
        "The dependency graph is acyclic.",
        "Proof Evidence is complete.",
        "Proof Integrity is valid.",
        "A partial Proof shall not support PROVEN, "
        "DISPROVEN, or CONTRADICTED.",
    ):
        assert requirement in content


def test_proof_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Proof Identifier validity.",
        "Proof Version support.",
        "Lifecycle Status validity.",
        "Proof Type validity.",
        "Reasoning Request resolution.",
        "Goal Assertion resolution.",
        "Conclusion resolution.",
        "Reasoning Outcome compatibility.",
        "Source Fact closure.",
        "Premise closure.",
        "Rule Application closure.",
        "Variable Binding closure.",
        "Proof Step dependency acyclicity.",
        "Reasoning Depth consistency.",
        "Canonical serialization.",
        "Proof Evidence completeness.",
        "Proof Integrity.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content
    assert (
        "An invalid Proof shall not support a terminal "
        "normative Reasoning Outcome."
    ) in content


def test_proof_validation_result_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Proof Validation shall produce exactly "
        "one deterministic Proof Validation Result."
    ) in content

    assert (
        "Permitted Proof Validation Result values are: PASS. FAIL."
    ) in content

    for property_name in (
        "Validation Identifier.",
        "Proof Identifier.",
        "Proof Version.",
        "Validation Outcome.",
        "Validated Proof Step Count.",
        "Detected Violations.",
        "Failure Classifications.",
        "Failure Reasons.",
        "Validation Evidence Reference.",
        "Validation Integrity Reference.",
    ):
        assert property_name in content


def test_proof_evidence_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Proof shall possess one deterministic "
        "Proof Evidence Reference."
    ) in content

    assert (
        "No valid or invalid Proof shall omit "
        "deterministic validation evidence."
    ) in content


def test_proof_step_evidence_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Proof Step shall possess one deterministic "
        "Step Evidence Reference."
    ) in content

    assert "No valid or invalid Proof Step shall omit evidence." in content


def test_proof_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Proof shall possess one deterministic "
        "Proof Integrity Reference."
    ) in content

    assert (
        "Any normative Proof mutation shall invalidate "
        "the Proof Integrity Reference."
    ) in content


def test_proof_step_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Proof Step shall possess one deterministic "
        "Step Integrity Reference."
    ) in content

    assert (
        "Any normative Proof Step mutation shall "
        "invalidate Step Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Use deterministic property ordering.",
        "Use deterministic reference ordering.",
        "Preserve Proof Type.",
        "Preserve Assertion Polarity.",
        "Preserve ordered Proof Steps.",
        "Preserve dependency references.",
        "Preserve Fact references.",
        "Preserve Premise references.",
        "Preserve Rule Application references.",
        "Preserve Variable Bindings.",
        "Preserve intermediate Conclusions.",
        "Preserve Reasoning Depth.",
        "Exclude non-normative presentation metadata.",
        "Canonical serialization shall be suitable for "
        "integrity calculation.",
    ):
        assert requirement in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Fact Identifier.",
        "Premise Priority. Then Premise Identifier.",
        "Reasoning Depth. Then Rule Priority. Then Rule Identifier. "
        "Then Rule Application Identifier.",
        "Variable Identifier.",
        "Reasoning Depth. Then Conclusion Identifier.",
        "Proof Step Position. Then Proof Step Identifier.",
        "Runtime discovery order shall not affect "
        "normative Proof ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "The Proof Identifier is missing, malformed, "
        "duplicated, or improperly reused.",
        "The primary Conclusion cannot be resolved.",
        "A mandatory Premise is unresolved or unsatisfied.",
        "A Rule Application is unresolved, invalid, "
        "non-applicable, failed, or cancelled.",
        "A circular Proof Step dependency exists.",
        "Maximum Reasoning Depth is exceeded.",
        "A DIRECT PROOF does not contain exactly one Proof Step.",
        "A CONTRADICTION PROOF omits either required Proof branch.",
        "Proof completeness cannot be established.",
        "Canonical serialization cannot be produced.",
        "Proof Evidence cannot be produced.",
        "Proof Integrity cannot be established.",
        "The Proof attempts to mutate source knowledge "
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
        "Register a Conclusion as a Graph Fact.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Modify a Query Result.",
        "Modify a registered Fact.",
        "Modify a registered Premise.",
        "Modify a registered Rule.",
        "Modify a Rule Application.",
        "Modify a Variable Binding.",
        "Modify a Derived Conclusion.",
        "Modify an Execution Context.",
        "Repair a broken Proof dependency.",
        "Resolve a contradiction by deleting evidence.",
        "Modify HAS Foundation 1.0 LTS.",
        "Modify Specification Runtime 1.0.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Modify CKP-005.1.",
        "Modify CKP-005.2.",
        "Modify CKP-005.3.",
        "Modify CKP-005.4.",
        "Modify CKP-005.5.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_proof_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in PROOF_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Proof Identity is valid and unique.",
        "Proof Version is supported.",
        "Exactly one canonical Proof Type is declared.",
        "Exactly one primary Conclusion is supported.",
        "Every Proof Step has unique identity and position.",
        "Every Proof Step references exactly one valid "
        "Rule Application.",
        "Every dependency is resolved and acyclic.",
        "Every mandatory Premise is satisfied.",
        "Every Rule Application is valid and APPLIED.",
        "Reasoning Depth is consistent and within limits.",
        "Proof completeness is established.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "Proof Evidence is complete.",
        "Proof Integrity is valid.",
        "No Failure Condition remains open.",
        "The Proof does not mutate source knowledge or "
        "a frozen baseline.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert "Version 1.0 defines the canonical Commerce Proof Model." in content

    assert (
        "Future implementations shall preserve this "
        "normative Proof contract."
    ) in content

    for excluded_capability in (
        "Production theorem prover.",
        "Production reasoning engine.",
        "Automated proof search.",
        "Proof optimization.",
        "Proof compression.",
        "Distributed proof construction.",
        "Interactive proof authoring.",
        "Persistence implementation.",
        "Transport implementation.",
        "Graph mutation.",
        "Ontology mutation.",
        "Machine learning.",
        "Probabilistic proof.",
    ):
        assert excluded_capability in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.7" in content
    assert "Reasoning Evidence Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
