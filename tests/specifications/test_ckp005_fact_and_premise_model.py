"""
Executable Specification

CKP-005.5
Commerce Fact and Premise Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_FACT_AND_PREMISE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Fact Identity",
    "## Fact Version",
    "## Fact Lifecycle",
    "## Fact Type",
    "## Fact Properties",
    "## Fact Source",
    "## Fact Provenance",
    "## Fact Confidence",
    "## Fact Integrity",
    "## Fact Evidence",
    "## Premise Identity",
    "## Premise Version",
    "## Premise Type",
    "## Premise Properties",
    "## Premise Source Reference",
    "## Premise Validation",
    "## Premise Satisfaction",
    "## Premise Evidence",
    "## Premise Integrity",
    "## Fact–Premise Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Validation Result",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Fact and Premise Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

FACT_TYPES = (
    "OBSERVED.",
    "DERIVED.",
    "ASSERTED.",
    "IMPORTED.",
)

FACT_LIFECYCLE_VALUES = (
    "Draft.",
    "Approved.",
    "Deprecated.",
    "Retired.",
)

PREMISE_TYPES = (
    "MANDATORY.",
    "OPTIONAL.",
    "NEGATIVE.",
    "DERIVED.",
)

FAILURE_CLASSIFICATIONS = (
    "FACT_IDENTITY_VIOLATION.",
    "FACT_VERSION_VIOLATION.",
    "FACT_TYPE_VIOLATION.",
    "FACT_SOURCE_VIOLATION.",
    "FACT_PROVENANCE_VIOLATION.",
    "FACT_CONFIDENCE_VIOLATION.",
    "FACT_INTEGRITY_VIOLATION.",
    "FACT_EVIDENCE_VIOLATION.",
    "PREMISE_IDENTITY_VIOLATION.",
    "PREMISE_VERSION_VIOLATION.",
    "PREMISE_TYPE_VIOLATION.",
    "PREMISE_REFERENCE_VIOLATION.",
    "PREMISE_VALIDATION_VIOLATION.",
    "PREMISE_SATISFACTION_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Fact Identity.",
    "Canonical Premise Identity.",
    "Fact Integrity.",
    "Premise Integrity.",
    "Evidence Completeness.",
    "Source Traceability.",
    "Deterministic Ordering.",
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
    assert "Title Commerce Fact and Premise Model" in content
    assert "Abbreviation CFPM" in content
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


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]

    assert len(headings) == len(set(headings))


def test_purpose_is_declared() -> None:
    content = normalized_text()

    assert (
        "Define the canonical, deterministic, immutable, "
        "evidence-producing, integrity- preserving, and "
        "auditable Fact and Premise Model for the Commerce "
        "Knowledge Platform."
    ) in content

    for boundary in (
        "It does not implement storage.",
        "It does not implement inference.",
        "It does not implement graph mutation.",
        "It does not implement reasoning execution.",
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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "No dependency shall be modified by this specification." in content


def test_fact_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Fact shall possess exactly one immutable "
        "Fact Identifier.",
        "CKP-FACT-000001",
        "Fact Identifiers shall be globally unique.",
        "Fact Identity shall remain stable throughout "
        "its lifecycle.",
        "Fact Identity shall never be reused.",
        "Missing, duplicated, malformed, or reused Fact "
        "Identifiers shall invalidate the Fact.",
    ):
        assert requirement in content


def test_fact_version_is_declared() -> None:
    content = normalized_text()

    assert "Every Fact shall declare one Fact Version." in content
    assert "The initial supported version is: 1.0." in content
    assert "Fact Version identifies the normative Fact schema." in content
    assert "Unsupported versions shall fail validation." in content


def test_fact_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in FACT_LIFECYCLE_VALUES:
        assert lifecycle in content

    assert "Only Approved Facts may participate in Reasoning." in content
    assert (
        "Lifecycle Status shall remain immutable during "
        "Reasoning execution."
    ) in content


def test_fact_types_are_declared() -> None:
    content = normalized_text()

    for fact_type in FACT_TYPES:
        assert fact_type in content

    assert "Every Fact shall declare exactly one Fact Type." in content
    assert "Unknown Fact Types shall be invalid." in content


def test_fact_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Fact Identifier.",
        "Fact Version.",
        "Fact Type.",
        "Lifecycle Status.",
        "Subject.",
        "Predicate.",
        "Object or Literal Value.",
        "Assertion Type.",
        "Assertion Polarity.",
        "Graph Scope.",
        "Evidence Reference.",
        "Integrity Reference.",
        "Source Reference.",
        "Timestamp.",
    ):
        assert property_name in content

    assert "Every mandatory property shall be explicit." in content
    assert "No mandatory property shall be inferred." in content


def test_fact_source_is_exactly_one() -> None:
    content = normalized_text()

    assert "Every Fact shall reference exactly one Fact Source." in content

    for property_name in (
        "Source Identifier.",
        "Source Type.",
        "Source Version.",
        "Source Integrity Reference.",
    ):
        assert property_name in content

    assert "Unknown Fact Sources shall invalidate the Fact." in content


def test_fact_provenance_is_complete_and_immutable() -> None:
    content = normalized_text()

    assert "Every Fact shall preserve complete provenance." in content

    for provenance_property in (
        "Origin.",
        "Collection Method.",
        "Observation Timestamp.",
        "Responsible System.",
        "Evidence Chain.",
    ):
        assert provenance_property in content

    assert "Fact Provenance shall remain immutable." in content


def test_fact_confidence_is_explicit_and_non_semantic() -> None:
    content = normalized_text()

    for requirement in (
        "Every Fact shall declare one Confidence Level.",
        "Confidence shall be explicitly declared.",
        "Confidence shall not modify Fact semantics.",
        "Confidence shall not influence deterministic Reasoning.",
    ):
        assert requirement in content


def test_fact_integrity_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Every Fact shall possess one deterministic "
        "Integrity Reference.",
        "Integrity shall bind every normative Fact property.",
        "Any normative mutation shall invalidate Fact Integrity.",
    ):
        assert requirement in content


def test_fact_evidence_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Every Fact shall possess one Evidence Reference.",
        "Evidence shall be deterministic.",
        "Evidence shall be complete.",
        "Evidence shall remain immutable.",
    ):
        assert requirement in content


def test_premise_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Premise shall possess exactly one immutable "
        "Premise Identifier.",
        "CKP-PREMISE-000001",
        "Premise Identifiers shall be globally unique.",
        "Premise Identity shall never be reused.",
    ):
        assert requirement in content


def test_premise_version_is_declared() -> None:
    content = normalized_text()

    assert "Every Premise shall declare one Premise Version." in content
    assert "Unsupported versions shall invalidate the Premise." in content


def test_premise_types_are_declared() -> None:
    content = normalized_text()

    for premise_type in PREMISE_TYPES:
        assert premise_type in content

    assert "Every Premise shall declare exactly one Premise Type." in content
    assert "Unknown Premise Types shall be invalid." in content


def test_premise_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Premise Identifier.",
        "Premise Version.",
        "Premise Type.",
        "Lifecycle Status.",
        "Referenced Fact.",
        "Validation Reference.",
        "Evidence Reference.",
        "Integrity Reference.",
        "Priority.",
        "Optionality.",
    ):
        assert property_name in content

    assert "Every mandatory property shall be explicit." in content


def test_premise_source_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Premise shall reference exactly one Fact Source.",
        "Premises shall not invent Facts.",
        "Premises shall reference only validated Facts.",
    ):
        assert requirement in content


def test_premise_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Premise Identity.",
        "Referenced Fact.",
        "Fact Integrity.",
        "Fact Evidence.",
        "Fact Lifecycle.",
        "Fact Version.",
        "Premise Version.",
        "Premise Type.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_premise_satisfaction_is_declared() -> None:
    content = normalized_text()

    assert "A Premise is satisfied only when:" in content

    for condition in (
        "Referenced Fact exists.",
        "Referenced Fact is Approved.",
        "Referenced Fact Integrity is valid.",
        "Referenced Fact Evidence is complete.",
        "Referenced Fact satisfies every Rule requirement.",
        "Otherwise the Premise shall be considered unsatisfied.",
    ):
        assert condition in content


def test_premise_evidence_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Every Premise shall preserve deterministic Evidence.",
        "Premise Evidence shall reference the underlying "
        "Fact Evidence.",
        "Premise Evidence shall remain immutable.",
    ):
        assert requirement in content


def test_premise_integrity_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Every Premise shall possess one deterministic "
        "Integrity Reference.",
        "Integrity shall bind every normative Premise property.",
        "Any mutation shall invalidate Premise Integrity.",
    ):
        assert requirement in content


def test_fact_premise_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Every Premise shall reference one or more Facts.",
        "Every Fact may participate in zero or more Premises.",
        "A Premise shall never create a Fact.",
        "A Fact shall never be rewritten by a Premise.",
        "Relationships shall be deterministic.",
        "Relationships shall be traceable.",
    ):
        assert relationship in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Facts and Premises shall possess canonical serialization.",
        "Preserve every normative property.",
        "Use deterministic ordering.",
        "Exclude presentation metadata.",
        "Produce identical output for equivalent structures.",
        "Canonical serialization shall support integrity calculation.",
    ):
        assert requirement in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Facts shall be ordered by: Fact Identifier.",
        "Premises shall be ordered by: Priority. "
        "Then Premise Identifier.",
        "Runtime ordering shall not affect normative ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_validation_result_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every validation shall produce exactly one "
        "Validation Result.",
        "Permitted values are: PASS. FAIL.",
        "Validation Results shall remain immutable.",
    ):
        assert requirement in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Fact Identity is invalid.",
        "Fact Version is unsupported.",
        "Fact Source cannot be resolved.",
        "Fact Integrity is invalid.",
        "Fact Evidence is incomplete.",
        "Premise Identity is invalid.",
        "Referenced Fact cannot be resolved.",
        "Premise Validation fails.",
        "Premise Satisfaction fails.",
        "Canonical Serialization cannot be produced.",
        "A frozen baseline is modified.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Canonical Commerce Term.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Modify CKP-004.",
        "Modify CKP-005.1.",
        "Modify CKP-005.2.",
        "Modify CKP-005.3.",
        "Modify CKP-005.4.",
        "Modify a registered Fact.",
        "Modify a registered Premise.",
        "Modify a registered Rule.",
        "Modify a registered Constraint.",
        "Modify an Execution Context.",
        "Rewrite Graph Knowledge.",
        "Repair missing Facts.",
        "Repair Premises.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Every Fact possesses unique identity.",
        "Every Premise possesses unique identity.",
        "Every referenced Fact is valid.",
        "Evidence is complete.",
        "Integrity is valid.",
        "Canonical Serialization succeeds.",
        "Deterministic Ordering succeeds.",
        "No Failure Condition remains open.",
        "No frozen baseline is modified.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Fact and Premise Model."
    ) in content

    assert (
        "Future implementations shall preserve this "
        "normative contract."
    ) in content

    for excluded_capability in (
        "Reasoning Engine.",
        "Inference Execution.",
        "Rule Scheduling.",
        "Persistence.",
        "Distributed Execution.",
        "Machine Learning.",
        "Probabilistic Reasoning.",
    ):
        assert excluded_capability in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005.6" in content
    assert "Proof Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
