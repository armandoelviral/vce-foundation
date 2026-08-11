from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]

CANONICAL = ROOT / "architecture" / "ARCHITECTURE_PRINCIPLE_CLASSIFICATION.md"
FREEZE = ROOT / "architecture" / "APC001_CLASSIFICATION_FREEZE.md"

RESEARCH_ROOT = (
    ROOT
    / "research"
    / "foundation"
    / "architecture_principles"
    / "apc001_classification"
)

CYCLE_1 = RESEARCH_ROOT / "APC001_REFUTATION_CYCLE_1.md"
CYCLE_2 = RESEARCH_ROOT / "APC001_REFUTATION_CYCLE_2_ADVERSARIAL.md"
CYCLE_3 = RESEARCH_ROOT / "APC001_REFUTATION_CYCLE_3_MINIMALITY.md"
CYCLE_4 = RESEARCH_ROOT / "APC001_REFUTATION_CYCLE_4_FINAL_ADVERSARIAL.md"
COVERAGE = RESEARCH_ROOT / "APC001_SL001_EVOLUTION_COVERAGE_TEST.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(content: str) -> str:
    return " ".join(content.split())


def canonical_text() -> str:
    return text(CANONICAL)


def freeze_text() -> str:
    return text(FREEZE)


def test_apc001_files_exist() -> None:
    for path in (
        CANONICAL,
        FREEZE,
        CYCLE_1,
        CYCLE_2,
        CYCLE_3,
        CYCLE_4,
        COVERAGE,
    ):
        assert path.is_file(), f"missing required APC-001 artifact: {path}"


def test_apc001_identity() -> None:
    content = normalized(canonical_text())

    assert "Identifier APC-001" in content
    assert "Version 1.0" in content
    assert "Status Normative" in content
    assert "Architecture Principle Classification Baseline" in content


def test_apc001_declares_promoted_authority() -> None:
    content = normalized(canonical_text())

    assert "Baseline 1.0" in content
    assert "Authority AUTHORITATIVE." in content
    assert "Authority Scope Architecture Principle Classification only." in content
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_apc001_preserves_promoted_source_identity() -> None:
    content = normalized(canonical_text())

    assert "Source Candidate APC-001 Version 0.4." in content


def test_apc001_declares_classification_boundary() -> None:
    content = normalized(canonical_text())

    assert "Classification Boundary" in content
    assert (
        "Does this proposition qualify for further "
        "Architecture Principle maturation?"
        in content
    )

    assert "Should authority be granted?" in content
    assert "What Version Authority does the principle possess?" in content


def test_apc001_declares_fourteen_criteria() -> None:
    content = canonical_text()

    identifiers = re.findall(
        r"^# Criterion (\d+) —",
        content,
        flags=re.MULTILINE,
    )

    assert identifiers == [
        str(i)
        for i in range(1, 15)
    ]


def test_apc001_criteria_have_expected_names() -> None:
    content = canonical_text()

    expected = (
        "Architectural Necessity",
        "Layer Correctness",
        "Semantic Independence",
        "Explicit Scope",
        "Applicability Boundary",
        "Cross-Decision Value",
        "Candidate Minimality",
        "Semantic Cohesion",
        "Falsifiability",
        "Evidence Basis",
        "Compatibility",
        "Set-Level Minimality",
        "Replaceability of Form",
        "Evolution Conformance",
    )

    for index, name in enumerate(expected, start=1):
        assert f"# Criterion {index} — {name}" in content


def test_apc001_declares_two_constitutional_conformance_tests() -> None:
    content = canonical_text()

    identifiers = re.findall(
        r"^## Conformance Test (\d+) —",
        content,
        flags=re.MULTILINE,
    )

    assert identifiers == ["1", "2"]

    assert "Technology Independence" in content
    assert "Authority Non-Expansion" in content


def test_apc001_conformance_tests_do_not_create_authority() -> None:
    content = normalized(canonical_text())

    assert "Constitutional Conformance Tests" in content
    assert (
        "These tests do not create new architectural authority."
        in content
    )


def test_apc001_declares_six_analysis_operations() -> None:
    content = canonical_text()

    operations = (
        "Reduction",
        "Equivalence Analysis",
        "Overlap Analysis",
        "Subsumption Analysis",
        "Composition Analysis",
        "Relocation Analysis",
    )

    for operation in operations:
        assert f"## {operation}" in content


def test_analysis_operations_are_not_criteria() -> None:
    content = normalized(canonical_text())

    assert (
        "The following are analysis operations, "
        "not independent classification criteria."
        in content
    )


def test_apc001_declares_sixteen_primary_outcomes() -> None:
    content = canonical_text()

    section = content.split("# Classification Outcomes", 1)[1]
    section = section.split("# Compatibility Outcomes", 1)[0]

    outcomes = (
        "ARCHITECTURE_PRINCIPLE_CANDIDATE.",
        "REDUCE.",
        "RELOCATE_TO_SPECIFICATION.",
        "RELOCATE_TO_RUNTIME.",
        "RELOCATE_TO_ARTIFACT.",
        "RELOCATE_TO_SECURITY.",
        "RELOCATE_TO_DOMAIN.",
        "RELOCATE_TO_IMPLEMENTATION.",
        "RELOCATE_TO_RESEARCH.",
        "RELOCATE_TO_COMMERCIAL.",
        "REDUNDANT_WITH_CONSTITUTION.",
        "REDUNDANT_WITH_EXISTING_AP.",
        "SUBSUMED.",
        "INCOMPATIBLE.",
        "REFUTED.",
        "INSUFFICIENT_EVIDENCE.",
    )

    for outcome in outcomes:
        assert re.search(
            rf"^{re.escape(outcome)}$",
            section,
            flags=re.MULTILINE,
        )

    matches = re.findall(
        r"^(?:"
        r"ARCHITECTURE_PRINCIPLE_CANDIDATE|"
        r"REDUCE|"
        r"RELOCATE_TO_SPECIFICATION|"
        r"RELOCATE_TO_RUNTIME|"
        r"RELOCATE_TO_ARTIFACT|"
        r"RELOCATE_TO_SECURITY|"
        r"RELOCATE_TO_DOMAIN|"
        r"RELOCATE_TO_IMPLEMENTATION|"
        r"RELOCATE_TO_RESEARCH|"
        r"RELOCATE_TO_COMMERCIAL|"
        r"REDUNDANT_WITH_CONSTITUTION|"
        r"REDUNDANT_WITH_EXISTING_AP|"
        r"SUBSUMED|"
        r"INCOMPATIBLE|"
        r"REFUTED|"
        r"INSUFFICIENT_EVIDENCE"
        r")\.$",
        section,
        flags=re.MULTILINE,
    )

    assert len(matches) == 16

def test_apc001_declares_seven_compatibility_outcomes() -> None:
    content = canonical_text()

    outcomes = (
        "COMPATIBLE.",
        "COMPATIBLE_WITH_SCOPE.",
        "DEPENDENT.",
        "PARTIALLY_OVERLAPPING.",
        "SUBSUMED.",
        "CONFLICTING.",
        "UNRESOLVED.",
    )

    section = content.split("# Compatibility Outcomes", 1)[1]
    section = section.split("# Conflict Boundary", 1)[0]

    for outcome in outcomes:
        assert re.search(
            rf"^{re.escape(outcome)}$",
            section,
            flags=re.MULTILINE,
        )


def test_subject_matter_does_not_determine_layer() -> None:
    content = normalized(canonical_text())

    assert "Subject matter shall not determine normative layer." in content


def test_runtime_subject_can_still_be_architectural() -> None:
    content = normalized(canonical_text())

    assert "Runtime Architecture." in content
    assert "Subject matter shall not determine normative layer." in content


def test_artifact_subject_can_still_be_architectural() -> None:
    content = normalized(canonical_text())

    assert "Artifact Architecture." in content


def test_apc001_supports_bounded_scope() -> None:
    content = normalized(canonical_text())

    assert "Technology-bounded Architecture." in content
    assert "Scope shall not be inferred." in content


def test_apc001_supports_conditional_applicability() -> None:
    content = normalized(canonical_text())

    assert "A candidate may be conditional." in content
    assert "Applicability conditions shall be" in content


def test_apc001_requires_cross_decision_value() -> None:
    content = normalized(canonical_text())

    assert (
        "An Architecture Principle shall constrain "
        "more than one architectural decision"
        in content
    )


def test_candidate_minimality_is_explicit() -> None:
    content = normalized(canonical_text())

    assert "Candidate Minimality" in content
    assert (
        "The candidate shall contain only the architectural "
        "semantics required for the principle."
        in content
    )


def test_semantic_cohesion_is_explicit() -> None:
    content = normalized(canonical_text())

    assert "Semantic Cohesion" in content
    assert "one coherent architectural proposition" in content


def test_semantic_independence_checks_equivalence_overlap_and_subsumption() -> None:
    content = normalized(canonical_text())

    for concept in (
        "Equivalence.",
        "Overlap.",
        "Containment.",
        "Subsumption.",
        "Partial derivation.",
        "Existing authority.",
    ):
        assert concept in content


def test_falsifiability_is_required() -> None:
    content = normalized(canonical_text())

    assert "Falsifiability" in content

    for outcome in (
        "Refute it.",
        "Narrow it.",
        "Relocate it.",
        "Demonstrate that it is unnecessary.",
    ):
        assert outcome in content


def test_evidence_must_be_scope_matched_and_non_circular() -> None:
    content = normalized(canonical_text())

    assert "Evidence shall be:" in content
    assert "Relevant." in content
    assert "Scope-matched." in content
    assert "Non-circular." in content


def test_compatibility_includes_composition() -> None:
    content = normalized(canonical_text())

    assert "Compatibility analysis shall include:" in content
    assert "Composition." in content

    assert (
        "Independent candidate validity shall not establish "
        "combined validity."
        in content
    )


def test_set_level_minimality_is_required() -> None:
    content = normalized(canonical_text())

    assert "Set-Level Minimality" in content

    for risk in (
        "Duplication.",
        "Artificial fragmentation.",
        "Over-aggregation.",
        "Contradiction.",
        "Subsumption.",
        "Semantic overlap.",
    ):
        assert risk in content


def test_replaceability_of_form_is_required() -> None:
    content = normalized(canonical_text())

    assert "Replaceability of Form" in content

    for form in (
        "Diagram.",
        "Component name.",
        "Repository path.",
        "Framework.",
        "Code structure.",
        "Class hierarchy.",
        "Deployment topology.",
    ):
        assert form in content


def test_evolution_is_conformance_not_independent_lifecycle() -> None:
    content = normalized(canonical_text())

    assert "Evolution Conformance" in content
    assert (
        "The candidate shall not define its own independent lifecycle "
        "merely because it is an Architecture Principle."
        in content
    )


def test_technology_independence_remains_constitutional_conformance() -> None:
    content = normalized(canonical_text())

    assert "Technology Independence" in content

    assert (
        "Such scope shall remain subordinate to broader "
        "constitutional Technology Independence."
        in content
    )


def test_authority_non_expansion_is_explicit() -> None:
    content = normalized(canonical_text())

    assert "Authority Non-Expansion" in content

    for forbidden in (
        "Override RC-001.",
        "Override constitutional authority.",
        "Create domain authority.",
        "Create Version Authority.",
        "Create Promotion Authority.",
        "Create implementation authority.",
    ):
        assert forbidden in content


def test_implementation_relocation_exists() -> None:
    content = normalized(canonical_text())

    assert "Implementation Relocation Boundary" in content
    assert "RELOCATE_TO_IMPLEMENTATION" in content


def test_implementation_examples_do_not_become_architecture() -> None:
    content = normalized(canonical_text())

    for example in (
        "Dependency injection.",
        "Specific class hierarchies.",
        "Internal caching strategies.",
        "Concrete compilation techniques.",
        "Language-specific idioms.",
    ):
        assert example in content

    assert (
        "They shall not become Architecture Principles "
        "without independent architecture-level semantics."
        in content
    )


def test_classification_does_not_grant_authority() -> None:
    content = normalized(canonical_text())

    assert "Promotion Boundary" in content
    assert (
        "Passing APC-001 does not grant Architecture Principle authority."
        in content
    )

    assert (
        "Classification establishes candidate suitability only."
        in content
    )


def test_conflict_boundary_rejects_implicit_precedence() -> None:
    content = normalized(canonical_text())

    assert "Conflict Boundary" in content

    for forbidden in (
        "Identifier.",
        "File order.",
        "Repository path.",
        "Age.",
        "Popularity.",
        "Implementation adoption.",
        "Specificity.",
        "Recency.",
    ):
        assert forbidden in content

    assert (
        "Conflict resolution between authoritative Architecture Principles "
        "remains external to APC-001."
        in content
    )


def test_ap_set_evaluation_is_required() -> None:
    content = normalized(canonical_text())

    assert "Architecture Principle Set Evaluation" in content

    for requirement in (
        "Semantic duplication.",
        "Subsumption.",
        "Compatibility.",
        "Composition.",
        "Set-level minimality.",
    ):
        assert requirement in content


def test_external_authority_gap_is_explicit() -> None:
    content = normalized(canonical_text())

    assert "External Authority Gap" in content

    for state in (
        "Authoritative.",
        "Superseded.",
        "Withdrawn.",
        "Invalidated.",
    ):
        assert state in content

    assert (
        "This gap shall remain external to APC-001."
        in content
    )


def test_current_candidates_have_no_ap_authority() -> None:
    content = normalized(canonical_text())

    assert "Candidate A NON-AUTHORITATIVE." in content
    assert "Candidate B NON-AUTHORITATIVE." in content
    assert "Candidate C NON-AUTHORITATIVE." in content


def test_freeze_identity() -> None:
    content = normalized(freeze_text())

    assert "Identifier APC-001-FREEZE" in content
    assert "Version 1.0" in content
    assert "Status Active Freeze" in content
    assert "APC-001 Architecture Principle Classification Model Version 0.4" in content


def test_freeze_declares_active_promoted_authority() -> None:
    content = normalized(freeze_text())

    assert "Authority AUTHORITATIVE." in content
    assert "Authority Scope Architecture Principle Classification only." in content
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_freeze_declares_fourteen_criteria() -> None:
    content = freeze_text()

    identifiers = re.findall(
        r"^APC-(\d{2})$",
        content,
        flags=re.MULTILINE,
    )

    required = {
        f"{i:02d}"
        for i in range(1, 15)
    }

    assert required.issubset(set(identifiers))
    assert set(identifiers).issubset(required)


def test_freeze_declares_exactly_two_conformance_tests() -> None:
    content = normalized(freeze_text())

    assert "Exactly two Constitutional Conformance Tests are frozen." in content
    assert "Conformance Test 1 Technology Independence." in content
    assert "Conformance Test 2 Authority Non-Expansion." in content


def test_freeze_declares_exactly_six_operations() -> None:
    content = normalized(freeze_text())

    assert "Exactly six Analysis Operations are frozen." in content

    for operation in (
        "Reduction.",
        "Equivalence Analysis.",
        "Overlap Analysis.",
        "Subsumption Analysis.",
        "Composition Analysis.",
        "Relocation Analysis.",
    ):
        assert operation in content


def test_freeze_declares_sixteen_primary_outcomes() -> None:
    content = normalized(freeze_text())

    assert (
        "Exactly sixteen primary Classification Outcomes are frozen."
        in content
    )


def test_freeze_preserves_promotion_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Promotion Boundary" in content

    assert (
        "Passing APC-001 shall establish candidate suitability only."
        in content
    )


def test_freeze_preserves_conflict_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen Conflict Boundary" in content

    assert (
        "Conflict resolution shall remain external to APC-001."
        in content
    )


def test_freeze_preserves_external_authority_gap() -> None:
    content = normalized(freeze_text())

    assert "Frozen External Authority Gap" in content

    assert (
        "This gap shall remain visible. "
        "It shall not be silently resolved inside APC-001."
        in content
    )


def test_freeze_explicitly_does_not_freeze_candidate_abc() -> None:
    content = normalized(freeze_text())

    assert "Explicitly Not Frozen" in content

    for candidate in (
        "Candidate A Scope and Generalization Discipline.",
        "Candidate B Explicit Material Assumptions.",
        "Candidate C Normative / Implementation Separation.",
    ):
        assert candidate in content

    assert (
        "No Architecture Principle candidate is promoted by this Freeze."
        in content
    )


def test_freeze_declares_breaking_evolution() -> None:
    content = normalized(freeze_text())

    assert "Breaking Evolution" in content

    for required in (
        "Trigger.",
        "Investigation.",
        "Canonical specification.",
        "Review.",
        "Refutation.",
        "Compatibility analysis.",
        "Promotion evaluation.",
        "Authority transition.",
        "Version change.",
    ):
        assert required in content


def test_freeze_release_criteria_reference_executable_contract() -> None:
    content = normalized(freeze_text())

    assert "Release Criteria" in content
    assert "Executable Contract validation passes." in content
    assert "Repository diff validation passes." in content


def test_cycle_1_has_thirty_cases() -> None:
    content = text(CYCLE_1)

    cases = re.findall(
        r"^# AR-(\d{3}) —",
        content,
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 31)
    ]


def test_cycle_2_has_thirty_cases() -> None:
    content = text(CYCLE_2)

    cases = re.findall(
        r"^# AC-(\d{3}) —",
        content,
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 31)
    ]


def test_cycle_3_has_thirty_cases() -> None:
    content = text(CYCLE_3)

    cases = re.findall(
        r"^# MA-(\d{3}) —",
        content,
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 31)
    ]


def test_cycle_4_has_thirty_six_cases() -> None:
    content = text(CYCLE_4)

    cases = re.findall(
        r"^# FA-(\d{3}) —",
        content,
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 37)
    ]


def test_final_adversarial_cycle_reports_zero_regressions() -> None:
    content = normalized(text(CYCLE_4))

    assert "Cases Evaluated 36." in content
    assert "Classification Regressions 0." in content
    assert "Required New Criteria 0." in content
    assert "Required New Conformance Tests 0." in content
    assert "Required New Analysis Operations 0." in content
    assert "Required New Outcomes 0." in content


def test_sl001_coverage_has_fifteen_cases() -> None:
    content = text(COVERAGE)

    cases = re.findall(
        r"^# EC-(\d{3}) —",
        content,
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 16)
    ]


def test_sl001_coverage_refutes_independent_evolution_readiness() -> None:
    content = normalized(text(COVERAGE))

    assert "Target Criterion APC-22 Evolution Readiness." in content
    assert (
        "REFUTED AS INDEPENDENT CLASSIFICATION CRITERION."
        in content
    )
    assert "Replacement Evolution Conformance." in content


def test_apc001_contract_does_not_resolve_external_authority_gap() -> None:
    canonical = normalized(canonical_text())
    freeze = normalized(freeze_text())

    assert "External Authority Gap" in canonical
    assert "Frozen External Authority Gap" in freeze

    assert "Promotion Boundary" in canonical
    assert "Frozen Promotion Boundary" in freeze

    assert "Conflict Boundary" in canonical
    assert "Frozen Conflict Boundary" in freeze
