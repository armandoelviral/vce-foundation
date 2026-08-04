"""
Executable Specification

CKP-005.9
Commerce Reasoning Validation Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_REASONING_VALIDATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Validation Identity",
    "## Validation Version",
    "## Validation Lifecycle",
    "## Validation Scope",
    "## Validation Session",
    "## Validation Target",
    "## Validation Inputs",
    "## Validation Pipeline",
    "## Validation Stages",
    "## Validation Rules",
    "## Validation Result",
    "## Validation Report",
    "## Validation Traceability",
    "## Validation Completeness",
    "## Validation Determinism",
    "## Validation Integrity",
    "## Canonical Serialization",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Validation Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

VALIDATION_LIFECYCLE_VALUES = (
    "Draft.",
    "Executing.",
    "Validated.",
    "Invalid.",
    "Superseded.",
    "Archived.",
)

VALIDATION_TARGETS = (
    "Reasoning Request.",
    "Reasoning Execution.",
    "Proof.",
    "Reasoning Evidence.",
    "Explanation.",
    "Terminal Reasoning Result.",
)

VALIDATION_INPUTS = (
    "Reasoning Request.",
    "Resolved Facts.",
    "Resolved Premises.",
    "Inference Rules.",
    "Rule Applications.",
    "Variable Bindings.",
    "Derived Conclusions.",
    "Proofs.",
    "Reasoning Evidence.",
    "Explanation.",
    "Terminal Result.",
    "Execution Context.",
    "Specification Baseline.",
)

VALIDATION_PIPELINE = (
    "Identity Validation.",
    "Version Validation.",
    "Lifecycle Validation.",
    "Scope Validation.",
    "Dependency Validation.",
    "Input Validation.",
    "Rule Validation.",
    "Proof Validation.",
    "Evidence Validation.",
    "Explanation Validation.",
    "Integrity Validation.",
    "Determinism Validation.",
    "Result Validation.",
    "Certification Decision.",
)

STAGE_RESULTS = (
    "PASS.",
    "FAIL.",
    "SKIPPED.",
)

FAILURE_CLASSIFICATIONS = (
    "VALIDATION_IDENTITY_VIOLATION.",
    "VALIDATION_VERSION_VIOLATION.",
    "VALIDATION_LIFECYCLE_VIOLATION.",
    "VALIDATION_SCOPE_VIOLATION.",
    "DEPENDENCY_VIOLATION.",
    "INPUT_VIOLATION.",
    "RULE_VIOLATION.",
    "PROOF_VIOLATION.",
    "EVIDENCE_VIOLATION.",
    "EXPLANATION_VIOLATION.",
    "DETERMINISM_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

VALIDATION_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Validation Identity.",
    "Validation Version Preservation.",
    "Lifecycle Validity.",
    "Exactly One Validation Scope.",
    "Exactly One Validation Target.",
    "Deterministic Pipeline.",
    "Deterministic Rule Evaluation.",
    "Complete Traceability.",
    "Complete Validation.",
    "Integrity Preservation.",
    "Canonical Serialization.",
    "Fail-Closed Validation.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def level_two_headings() -> list[str]:
    return [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Validation Model" in content
    assert "Abbreviation CRVM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    headings = level_two_headings()

    for section in EXPECTED_SECTIONS:
        assert headings.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    headings = level_two_headings()

    positions = [
        headings.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = level_two_headings()

    assert len(headings) == len(set(headings))


def test_purpose_is_declared() -> None:
    content = normalized_text()

    assert (
        "Define the canonical, deterministic, immutable, "
        "independently verifiable, auditable, complete, "
        "traceable, fail-closed, and normatively executable "
        "Validation Model for the Commerce Knowledge Platform."
    ) in content

    assert (
        "The Commerce Reasoning Validation Model defines "
        "how a complete Reasoning Execution shall be "
        "evaluated against the normative requirements "
        "established by CKP-005."
    ) in content

    assert "Validation determines normative correctness." in content


def test_validation_does_not_execute_or_repair_reasoning() -> None:
    content = normalized_text()

    for boundary in (
        "Validation does not perform reasoning.",
        "Validation does not modify reasoning.",
        "Validation does not repair reasoning.",
        "Validation does not generate evidence.",
    ):
        assert boundary in content

    assert (
        "Validation verifies the integrity, completeness, "
        "consistency, determinism, and normative compliance "
        "of one Reasoning Execution."
    ) in content


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
        "CKP-005.6 Proof Model.",
        "CKP-005.7 Reasoning Evidence Model.",
        "CKP-005.8 Explanation Model.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content

    assert (
        "Validation shall never redefine or modify any dependency."
    ) in content


def test_validation_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Validation shall possess exactly one "
        "immutable Validation Identifier.",
        "CKP-VALIDATION-000001",
        "Validation Identity shall be globally unique.",
        "Validation Identity shall never be reused.",
        "Validation Identity shall remain independent "
        "from Validation Version.",
        "Missing, malformed, duplicated, or reused "
        "Validation Identity shall cause validation failure.",
    ):
        assert requirement in content


def test_validation_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Validation shall declare exactly one "
        "Validation Version.",
        "The initial supported Validation Version is: 1.0.",
        "Validation Version identifies the normative "
        "Validation schema.",
        "Unsupported Validation Versions shall fail validation.",
        "Validation Version shall not replace Validation Identity.",
    ):
        assert requirement in content


def test_validation_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in VALIDATION_LIFECYCLE_VALUES:
        assert lifecycle in content

    assert (
        "Every Validation shall declare exactly one "
        "Lifecycle Status."
    ) in content

    assert "Lifecycle Status shall not regress." in content

    assert (
        "Only Validated Validation artifacts shall "
        "support normative certification."
    ) in content


def test_validation_scope_is_exactly_one_execution() -> None:
    content = normalized_text()

    for requirement in (
        "Every Validation shall evaluate exactly one "
        "Reasoning Execution.",
        "Validation shall not combine multiple Reasoning Executions.",
        "Validation Scope shall remain immutable.",
        "Validation Scope shall explicitly identify the "
        "target Reasoning Request.",
    ):
        assert requirement in content


def test_validation_session_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Validation shall declare exactly one "
        "Validation Session."
    ) in content

    for property_name in (
        "Session Identifier.",
        "Session Version.",
        "Validation Timestamp.",
        "Execution Context Reference.",
        "Validation Engine Version.",
        "Specification Baseline.",
        "Session Integrity Reference.",
    ):
        assert property_name in content

    assert "A Validation Session shall remain immutable." in content


def test_validation_target_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Validation shall identify exactly one "
        "Validation Target."
    ) in content

    for target in VALIDATION_TARGETS:
        assert target in content

    assert "Unknown Validation Targets shall be invalid." in content


def test_validation_inputs_are_declared() -> None:
    content = normalized_text()

    for validation_input in VALIDATION_INPUTS:
        assert validation_input in content

    assert (
        "No undocumented input shall participate in Validation."
    ) in content


def test_validation_pipeline_is_canonical() -> None:
    content = normalized_text()

    assert (
        "Validation shall execute the following canonical pipeline:"
    ) in content

    for stage in VALIDATION_PIPELINE:
        assert stage in content

    assert "Pipeline ordering shall be deterministic." in content
    assert "Implementation-defined stages are prohibited." in content


def test_validation_pipeline_order_is_exact() -> None:
    content = normalized_text()

    expected_pipeline = (
        "Validation shall execute the following canonical pipeline: "
        "Identity Validation. Version Validation. "
        "Lifecycle Validation. Scope Validation. "
        "Dependency Validation. Input Validation. "
        "Rule Validation. Proof Validation. "
        "Evidence Validation. Explanation Validation. "
        "Integrity Validation. Determinism Validation. "
        "Result Validation. Certification Decision."
    )

    assert expected_pipeline in content


def test_validation_stage_results_are_declared() -> None:
    content = normalized_text()

    assert (
        "Every Validation Stage shall produce exactly "
        "one deterministic Stage Result."
    ) in content

    for result in STAGE_RESULTS:
        assert result in content

    assert "Every executed stage shall remain traceable." in content


def test_validation_rules_are_declared() -> None:
    content = normalized_text()

    for validation_rule in (
        "Identity correctness.",
        "Version compatibility.",
        "Lifecycle correctness.",
        "Dependency integrity.",
        "Input completeness.",
        "Reasoning consistency.",
        "Proof correctness.",
        "Evidence completeness.",
        "Explanation consistency.",
        "Determinism.",
        "Integrity.",
        "Canonical serialization.",
        "Read-only preservation.",
    ):
        assert validation_rule in content

    assert "Every Validation Rule shall be deterministic." in content


def test_validation_result_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Validation shall produce exactly one "
        "Validation Result."
    ) in content

    assert "Permitted Validation Result values are: PASS. FAIL." in content
    assert "Validation Result shall remain immutable." in content

    assert (
        "Validation Result shall summarize every mandatory "
        "Validation Rule."
    ) in content


def test_validation_report_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Validation shall produce exactly one "
        "Validation Report."
    ) in content

    for property_name in (
        "Validation Identifier.",
        "Validation Version.",
        "Validation Target.",
        "Validation Result.",
        "Executed Stages.",
        "Executed Rules.",
        "Detected Violations.",
        "Evidence References.",
        "Explanation References.",
        "Integrity Reference.",
    ):
        assert property_name in content

    assert "Validation Report shall remain immutable." in content


def test_validation_traceability_is_complete() -> None:
    content = normalized_text()

    for requirement in (
        "Every Validation decision shall be traceable "
        "to validated normative artifacts.",
        "Every Validation Rule shall identify the "
        "artifacts that justified its decision.",
        "No Validation Result shall exist without traceability.",
    ):
        assert requirement in content


def test_validation_completeness_is_declared() -> None:
    content = normalized_text()

    assert "Validation is complete only when:" in content

    for requirement in (
        "Every mandatory Validation Stage executes.",
        "Every mandatory Validation Rule executes.",
        "Every required artifact is evaluated.",
        "Every detected violation is reported.",
        "Integrity is verified.",
        "Determinism is verified.",
        "Certification Decision is produced.",
    ):
        assert requirement in content


def test_validation_determinism_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Equivalent Reasoning Executions shall produce "
        "equivalent Validation Results.",
        "Runtime scheduling shall not affect Validation Results.",
        "Execution timestamps shall not affect "
        "Validation equality.",
        "Implementation-specific ordering shall not "
        "affect Validation.",
    ):
        assert requirement in content


def test_validation_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Validation shall possess exactly one "
        "Validation Integrity Reference."
    ) in content

    for property_name in (
        "Validation Identity.",
        "Validation Version.",
        "Validation Target.",
        "Validation Result.",
        "Validation Report.",
        "Validation Rules.",
        "Validation Stages.",
        "Specification Baseline.",
    ):
        assert property_name in content

    assert (
        "Any normative mutation shall invalidate "
        "Validation Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Validation artifact shall possess one "
        "deterministic canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Target.",
        "Result.",
        "Stages.",
        "Rules.",
        "Report.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Presentation metadata shall be excluded." in content

    assert (
        "Canonical serialization shall be suitable for "
        "integrity calculation."
    ) in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Validation Identity is invalid.",
        "Validation Version is unsupported.",
        "Lifecycle Status is invalid.",
        "Validation Scope is ambiguous.",
        "Validation Target is invalid.",
        "Dependencies are incompatible.",
        "Mandatory inputs are missing.",
        "Validation Rules are violated.",
        "Proof validation fails.",
        "Evidence validation fails.",
        "Explanation validation fails.",
        "Integrity cannot be established.",
        "Determinism cannot be established.",
        "Canonical serialization cannot be produced.",
        "Read-only boundaries are violated.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Execute reasoning.",
        "Modify reasoning.",
        "Modify proofs.",
        "Modify evidence.",
        "Modify explanations.",
        "Modify ontology.",
        "Modify graph.",
        "Modify vocabulary.",
        "Modify immutable baselines.",
        "Repair invalid artifacts.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_validation_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in VALIDATION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Lifecycle permits validation.",
        "Scope is valid.",
        "Target is valid.",
        "Dependencies are compatible.",
        "Mandatory inputs are complete.",
        "All Validation Rules pass.",
        "Integrity is valid.",
        "Determinism is preserved.",
        "Canonical serialization succeeds.",
        "No Failure Condition remains open.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Reasoning Validation Model."
    ) in content

    for excluded_capability in (
        "Runtime optimization.",
        "Distributed validation.",
        "Cryptographic implementation.",
        "Machine learning.",
        "Probabilistic validation.",
        "Interactive validation.",
        "Visualization.",
    ):
        assert excluded_capability in content

    assert (
        "Future implementations shall preserve this "
        "normative Validation contract."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.10" in content
    assert "Reasoning Certification Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
