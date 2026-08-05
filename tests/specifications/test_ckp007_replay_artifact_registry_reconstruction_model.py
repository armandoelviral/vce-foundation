"""
Executable Specification

CKP-007.10
Commerce Replay Artifact Registry Reconstruction Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_ARTIFACT_REGISTRY_RECONSTRUCTION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Artifact Registry Reconstruction Identity",
    "## Artifact Registry Reconstruction Version",
    "## Artifact Registry Reconstruction Lifecycle",
    "## Artifact Registry Reconstruction Scope",
    "## Artifact Registry Reconstruction Inputs",
    "## Artifact Registry Reconstruction Preconditions",
    "## Historical Artifact Registry Reference",
    "## Registry Identity Reconstruction",
    "## Registry Version Reconstruction",
    "## Registry Lifecycle Reconstruction",
    "## Artifact Identity Reconstruction",
    "## Artifact Type Reconstruction",
    "## Artifact Version Reconstruction",
    "## Artifact Classification Reconstruction",
    "## Artifact Source Reconstruction",
    "## Artifact Ownership Reconstruction",
    "## Artifact Registration Reconstruction",
    "## Artifact Resolution Reconstruction",
    "## Artifact Reference Reconstruction",
    "## Artifact Relationship Reconstruction",
    "## Artifact Provenance Reconstruction",
    "## Artifact Evidence Reconstruction",
    "## Artifact Integrity Reconstruction",
    "## Artifact Immutability Reconstruction",
    "## Registry Ordering Reconstruction",
    "## Registry Closure Reconstruction",
    "## Registry Reconstruction Completeness",
    "## Registry Reconstruction Consistency",
    "## Registry Reconstruction Validation",
    "## Registry Reconstruction Integrity",
    "## Registry Reconstruction Traceability",
    "## Registry Reconstruction Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Artifact Registry Reconstruction Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Reconstructing.",
    "Validated.",
    "Completed.",
    "Archived.",
)

FAILURE_CLASSIFICATIONS = (
    "ARTIFACT_REGISTRY_RECONSTRUCTION_IDENTITY_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_VERSION_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_LIFECYCLE_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_SCOPE_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_INPUT_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_PRECONDITION_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_REFERENCE_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_ORDERING_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_COMPLETENESS_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_CONSISTENCY_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_INTEGRITY_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_TRACEABILITY_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_SERIALIZATION_VIOLATION.",
    "ARTIFACT_REGISTRY_RECONSTRUCTION_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Artifact Registry Reconstruction Identity.",
    "Exactly one Artifact Registry Reconstruction Version.",
    "Exactly one Historical Artifact Registry.",
    "Exactly one Reconstructed Artifact Registry.",
    "Deterministic Ordering.",
    "Closure Preservation.",
    "Completeness Preservation.",
    "Consistency Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Validation.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def headings() -> list[str]:
    return [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_identity() -> None:
    content = normalized_text()

    assert "# CKP-007" in content
    assert "Title Commerce Replay Artifact Registry Reconstruction Model" in content
    assert "Abbreviation CRARRM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_sections_exist_once() -> None:
    hs = headings()

    for section in EXPECTED_SECTIONS:
        assert hs.count(section) == 1


def test_section_order() -> None:
    assert tuple(headings()) == EXPECTED_SECTIONS


def test_lifecycle_states() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_fail_closed_validation() -> None:
    content = normalized_text()

    assert (
        "Artifact Registry Reconstruction Validation shall fail closed."
        in content
    )


def test_failure_classifications() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    assert "Artifact Registry Reconstruction shall not modify:" in content

    for target in (
        "Historical Artifact Registry.",
        "Historical Artifact Set.",
        "Historical Evidence.",
        "Historical Provenance.",
        "Frozen Baselines.",
    ):
        assert target in content


def test_invariants() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-007.11" in content
    assert "Replay Runtime Result Reconstruction Model." in content


def test_end_marker() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
