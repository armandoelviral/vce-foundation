"""
Executable Specification

CKP-005.2
Commerce Reasoning Structure Model

This specification validates the normative structure of:

research/commerce/reasoning/CKP005_REASONING_STRUCTURE_MODEL.md
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_REASONING_STRUCTURE_MODEL.md"
)


EXPECTED_TITLE = "# CKP-005"

EXPECTED_SECTIONS = [
    "# Structure Identity",
    "# Structural Scope",
    "# Canonical Reasoning Graph",
    "# Structural Components",
    "# Reasoning Request Node",
    "# Goal Assertion Node",
    "# Fact Set Node",
    "# Premise Set Node",
    "# Rule Registry Reference",
    "# Applicable Rule Set",
    "# Rule Application",
    "# Variable Binding Set",
    "# Derived Assertion Set",
    "# Proof Structure",
    "# Proof Step Structure",
    "# Evidence Structure",
    "# Explanation Structure",
    "# Reasoning Result Structure",
    "# Structural Relationships",
    "# Cardinality Rules",
    "# Lifecycle Rules",
    "# Structural Integrity",
    "# Canonical Serialization",
    "# Deterministic Ordering",
    "# Structural Invariants",
    "# Structural Validation",
    "# Failure Conditions",
    "# Read-Only Boundary",
    "# Success Criteria",
    "# Release Boundary",
    "# Next Deliverable",
]

CHARTER_CONCEPTS = [
    "Reasoning Request",
    "Goal Assertion",
    "Fact Set",
    "Premise Set",
    "Applicable Rule",
    "Rule Application",
    "Derived Assertion",
    "Proof",
    "Evidence",
    "Explanation",
    "Reasoning Result",
]


def load_document() -> str:
    return SPEC.read_text(encoding="utf-8")


def test_document_exists() -> None:
    assert SPEC.exists()


def test_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_document_identity() -> None:
    text = load_document()
    assert EXPECTED_TITLE in text
    assert "Commerce Reasoning Structure Model" in text
    assert "CRSM" in text
    assert "Version" in text
    assert "1.0" in text


def test_every_required_section_exists() -> None:
    text = load_document()

    for section in EXPECTED_SECTIONS:
        assert section in text, section


def test_sections_are_unique() -> None:
    text = load_document()

    for section in EXPECTED_SECTIONS:
        assert text.count(section) == 1, section


def test_canonical_section_order() -> None:
    text = load_document()

    positions = [
        text.index(section)
        for section in EXPECTED_SECTIONS
    ]

    assert positions == sorted(positions)


def test_structure_identity_first_section() -> None:
    text = load_document()

    title = text.index(EXPECTED_TITLE)
    identity = text.index("# Structure Identity")

    assert identity > title


def test_end_of_specification_exists() -> None:
    text = load_document()

    assert "# End of Specification" in text


def test_end_of_specification_is_last_marker() -> None:
    text = load_document().rstrip()

    assert text.endswith("# End of Specification")


def test_no_duplicate_end_marker() -> None:
    text = load_document()

    assert text.count("# End of Specification") == 1


def test_document_mentions_all_core_reasoning_components() -> None:
    text = load_document()

    for concept in CHARTER_CONCEPTS:
        assert concept in text, concept


def test_structure_contains_read_only_boundary() -> None:
    text = load_document()

    assert "# Read-Only Boundary" in text
    assert "read-only" in text.lower()


def test_structure_contains_success_criteria() -> None:
    text = load_document()

    assert "# Success Criteria" in text


def test_structure_contains_release_boundary() -> None:
    text = load_document()

    assert "# Release Boundary" in text


def test_structure_contains_next_deliverable() -> None:
    text = load_document()

    assert "# Next Deliverable" in text
    assert "CKP-005.3" in text


def test_structure_references_reasoning_request() -> None:
    text = load_document()

    assert "Reasoning Request" in text


def test_structure_references_goal_assertion() -> None:
    text = load_document()

    assert "Goal Assertion" in text


def test_structure_references_proof() -> None:
    text = load_document()

    assert "Proof" in text


def test_structure_references_evidence() -> None:
    text = load_document()

    assert "Evidence" in text


def test_structure_references_explanation() -> None:
    text = load_document()

    assert "Explanation" in text


def test_structure_references_reasoning_result() -> None:
    text = load_document()

    assert "Reasoning Result" in text


def test_coherence_with_ckp0051_charter() -> None:
    """
    CKP-005.2 specializes the charter and therefore
    shall preserve the core conceptual vocabulary.
    """

    text = load_document()

    required = [
        "Reasoning Execution",
        "Derived Assertion",
        "Applicable Rule",
        "Proof",
        "Evidence",
        "Explanation",
        "Reasoning Result",
        "deterministic",
        "immutable",
    ]

    lower = text.lower()

    for item in required:
        if item.islower():
            assert item in lower
        else:
            assert item in text


def test_no_duplicate_normative_sections() -> None:
    text = load_document()

    headings = [
        line
        for line in text.splitlines()
        if line.startswith("# ")
    ]

    assert len(headings) == len(set(headings))


def test_next_deliverable_points_to_ckp0053() -> None:
    text = load_document()

    index = text.index("# Next Deliverable")

    assert "CKP-005.3" in text[index:]
