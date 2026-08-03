"""
Executable Specification

CKP-005.8
Commerce Explanation Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_EXPLANATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Explanation Identity",
    "## Explanation Version",
    "## Explanation Lifecycle",
    "## Explanation Type",
    "## Explanation Properties",
    "## Explanation Scope",
    "## Explanation Audience",
    "## Explanation Granularity",
    "## Explanation Source References",
    "## Explanation Narrative",
    "## Explanation Structure",
    "## Explanation Sections",
    "## Explanation Ordering",
    "## Explanation Traceability",
    "## Explanation Completeness",
    "## Explanation Validation",
    "## Explanation Validation Result",
    "## Explanation Integrity",
    "## Canonical Serialization",
    "## Determinism",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Explanation Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

EXPLANATION_TYPES = (
    "SUMMARY.",
    "DETAILED.",
    "TRACE.",
    "CONTRADICTION.",
    "FAILURE.",
    "TERMINAL.",
)

LIFECYCLE_VALUES = (
    "Draft.",
    "Constructed.",
    "Validated.",
    "Invalid.",
    "Superseded.",
    "Archived.",
)

AUDIENCES = (
    "Human.",
    "Machine.",
    "Hybrid.",
)

GRANULARITY_LEVELS = (
    "Summary.",
    "Standard.",
    "Detailed.",
    "Trace.",
)

STRUCTURAL_SECTIONS = (
    "Introduction.",
    "Reasoning Context.",
    "Evidence Summary.",
    "Inference Summary.",
    "Proof Summary.",
    "Outcome Summary.",
    "References.",
)

FAILURE_CLASSIFICATIONS = (
    "EXPLANATION_IDENTITY_VIOLATION.",
    "EXPLANATION_VERSION_VIOLATION.",
    "EXPLANATION_LIFECYCLE_VIOLATION.",
    "EXPLANATION_TYPE_VIOLATION.",
    "TRACEABILITY_VIOLATION.",
    "COMPLETENESS_VIOLATION.",
    "ORDERING_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

EXPLANATION_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Explanation Identity.",
    "Version Preservation.",
    "Lifecycle Validity.",
    "Canonical Explanation Type.",
    "Exactly One Reasoning Scope.",
    "Semantic Equivalence.",
    "Complete Traceability.",
    "Deterministic Ordering.",
    "Canonical Serialization.",
    "Integrity Preservation.",
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
    assert "Title Commerce Explanation Model" in content
    assert "Abbreviation CEM" in content
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
        "traceable, auditable, human-consumable, "
        "machine-readable, and normatively verifiable "
        "Explanation Model for the Commerce Knowledge Platform."
    ) in content

    for rule in (
        "An Explanation shall communicate how a "
        "Reasoning Request produced one terminal "
        "Reasoning Outcome without altering the "
        "underlying reasoning process.",
        "An Explanation shall derive exclusively from "
        "validated normative artifacts.",
        "An Explanation shall preserve semantic "
        "equivalence with the underlying Reasoning Evidence.",
    ):
        assert rule in content


def test_non_implementation_boundary_is_declared() -> None:
    content = normalized_text()

    for boundary in (
        "The Explanation Model does not execute reasoning.",
        "It does not infer additional conclusions.",
        "It does not repair inconsistent evidence.",
        "It does not modify ontology, graph, or proof artifacts.",
    ):
        assert boundary in content


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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content

    assert (
        "An Explanation shall never redefine or modify "
        "any dependency."
    ) in content


def test_explanation_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Explanation shall possess exactly one "
        "immutable Explanation Identifier.",
        "CKP-EXPLANATION-000001",
        "Every Explanation Identifier shall be unique "
        "within one Reasoning Execution.",
        "An Explanation Identifier shall never be reused.",
        "A missing, malformed, duplicated, or reused "
        "Explanation Identifier shall cause validation failure.",
    ):
        assert requirement in content


def test_explanation_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Explanation shall declare one Explanation Version.",
        "The initial supported Explanation Version is: 1.0.",
        "Explanation Version identifies the normative "
        "Explanation schema.",
        "Explanation Version shall not replace Explanation Identity.",
        "Unsupported Explanation Versions shall cause "
        "validation failure.",
    ):
        assert requirement in content


def test_explanation_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in LIFECYCLE_VALUES:
        assert lifecycle in content

    assert (
        "Only a Validated Explanation may accompany a "
        "terminal Reasoning Result."
    ) in content

    assert "Lifecycle Status shall not regress." in content


def test_explanation_types_are_declared() -> None:
    content = normalized_text()

    for explanation_type in EXPLANATION_TYPES:
        assert explanation_type in content

    assert (
        "Every Explanation shall declare exactly one "
        "canonical Explanation Type."
    ) in content

    assert "Unknown Explanation Types shall be invalid." in content


def test_explanation_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Explanation Identifier.",
        "Explanation Version.",
        "Explanation Type.",
        "Lifecycle Status.",
        "Reasoning Request Identifier.",
        "Reasoning Outcome.",
        "Reasoning Status.",
        "Graph Identifier.",
        "Graph Version.",
        "Execution Context Reference.",
        "Evidence References.",
        "Proof References.",
        "Explanation Integrity Reference.",
    ):
        assert property_name in content


def test_explanation_scope_is_exactly_one_request_and_outcome() -> None:
    content = normalized_text()

    for requirement in (
        "Every Explanation shall belong to exactly one "
        "Reasoning Request.",
        "An Explanation shall explain exactly one "
        "terminal Reasoning Outcome.",
        "An Explanation shall not merge independent "
        "Reasoning Requests.",
        "Scope shall remain immutable.",
    ):
        assert requirement in content


def test_explanation_audience_is_explicit() -> None:
    content = normalized_text()

    assert "The intended audience shall be explicit." in content

    for audience in AUDIENCES:
        assert audience in content

    assert (
        "Audience selection shall not modify semantic meaning."
    ) in content


def test_explanation_granularity_is_explicit_and_non_semantic() -> None:
    content = normalized_text()

    assert "Explanation Granularity shall be explicit." in content

    for level in GRANULARITY_LEVELS:
        assert level in content

    assert "Granularity shall affect presentation only." in content
    assert "Granularity shall not alter semantic content." in content


def test_source_references_are_normative_and_validated() -> None:
    content = normalized_text()

    assert (
        "Every Explanation shall reference only "
        "validated normative artifacts."
    ) in content

    for artifact in (
        "Facts.",
        "Premises.",
        "Rules.",
        "Rule Applications.",
        "Proofs.",
        "Proof Steps.",
        "Reasoning Evidence.",
        "Contradiction Evidence.",
        "Failure Evidence.",
        "Terminal Evidence.",
    ):
        assert artifact in content

    assert "No undocumented source shall be introduced." in content


def test_explanation_narrative_is_semantically_equivalent() -> None:
    content = normalized_text()

    for requirement in (
        "Every Explanation shall provide one coherent narrative.",
        "The narrative shall preserve semantic equivalence "
        "with the underlying reasoning.",
        "The narrative shall not introduce new facts, "
        "premises, rules, or conclusions.",
    ):
        assert requirement in content


def test_explanation_structure_is_declared() -> None:
    content = normalized_text()

    assert "Every Explanation shall contain:" in content

    for section in STRUCTURAL_SECTIONS:
        assert section in content


def test_explanation_sections_are_unique_and_non_overlapping() -> None:
    content = normalized_text()

    for requirement in (
        "Each structural section shall appear exactly once.",
        "Sections shall not overlap semantically.",
        "Sections shall preserve deterministic order.",
    ):
        assert requirement in content


def test_explanation_ordering_is_canonical() -> None:
    content = normalized_text()

    expected_order = (
        "Explanation Sections shall appear in this order: "
        "Introduction. Reasoning Context. Evidence Summary. "
        "Inference Summary. Proof Summary. Outcome Summary. "
        "References."
    )

    assert expected_order in content
    assert "Implementation-defined ordering is prohibited." in content


def test_explanation_traceability_is_complete() -> None:
    content = normalized_text()

    for requirement in (
        "Every statement contained within an Explanation "
        "shall be traceable to one or more validated "
        "normative artifacts.",
        "No orphan explanation statement shall exist.",
        "Every referenced artifact shall resolve.",
    ):
        assert requirement in content


def test_explanation_completeness_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every referenced artifact resolves.",
        "Every normative statement is traceable.",
        "Reasoning Outcome is represented.",
        "Supporting Proof is represented when applicable.",
        "Supporting Evidence is represented.",
        "Failure Evidence is represented when applicable.",
        "Terminal Evidence is represented.",
    ):
        assert requirement in content


def test_explanation_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Type.",
        "Scope.",
        "Audience.",
        "Granularity.",
        "Traceability.",
        "Completeness.",
        "Ordering.",
        "Integrity.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_explanation_validation_result_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Explanation Validation shall produce "
        "exactly one deterministic Validation Result.",
        "Permitted values are: PASS. FAIL.",
        "Validation Results shall remain immutable.",
    ):
        assert requirement in content


def test_explanation_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Explanation shall possess exactly one "
        "Explanation Integrity Reference."
    ) in content

    for integrity_binding in (
        "Identity.",
        "Version.",
        "Type.",
        "Lifecycle.",
        "Reasoning Request.",
        "Reasoning Outcome.",
        "Evidence References.",
        "Proof References.",
        "Narrative Structure.",
    ):
        assert integrity_binding in content

    assert (
        "Any normative mutation shall invalidate "
        "Explanation Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Explanation shall possess one deterministic "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Type.",
        "Ordering.",
        "Narrative Structure.",
        "References.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Presentation metadata shall be excluded." in content

    assert (
        "Canonical serialization shall be suitable for "
        "integrity calculation."
    ) in content


def test_determinism_is_declared() -> None:
    content = normalized_text()

    assert (
        "Identical Reasoning Executions shall produce "
        "normatively identical Explanations."
    ) in content

    assert (
        "Presentation formatting shall not affect "
        "Explanation equality."
    ) in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Identity is invalid.",
        "Version is unsupported.",
        "Lifecycle is incompatible.",
        "Type is invalid.",
        "Traceability cannot be established.",
        "Completeness cannot be established.",
        "Ordering is non-deterministic.",
        "Canonical serialization cannot be produced.",
        "Integrity cannot be established.",
        "The Explanation attempts to modify source knowledge.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create ontology artifacts.",
        "Create graph artifacts.",
        "Create reasoning artifacts.",
        "Create proofs.",
        "Modify evidence.",
        "Modify reasoning outcomes.",
        "Modify ontology.",
        "Modify graph.",
        "Modify proof.",
        "Modify reasoning evidence.",
        "Modify immutable baselines.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_explanation_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in EXPLANATION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Lifecycle permits validation.",
        "Type is valid.",
        "Traceability is complete.",
        "Completeness is established.",
        "Ordering is deterministic.",
        "Canonical serialization succeeds.",
        "Integrity is valid.",
        "No Failure Condition remains open.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Explanation Model."
    ) in content

    for excluded_capability in (
        "Natural language optimization.",
        "Localization.",
        "Summarization algorithms.",
        "LLM integration.",
        "Interactive explanations.",
        "Visualization.",
        "Machine learning.",
        "Probabilistic explanations.",
    ):
        assert excluded_capability in content

    assert (
        "Future implementations shall preserve this "
        "normative contract."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.9" in content
    assert "Reasoning Validation Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
