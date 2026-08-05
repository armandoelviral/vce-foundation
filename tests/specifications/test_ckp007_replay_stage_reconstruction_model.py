"""
Executable Specification

CKP-007.8
Commerce Replay Stage Reconstruction Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_STAGE_RECONSTRUCTION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Stage Reconstruction Identity",
    "## Stage Reconstruction Version",
    "## Stage Reconstruction Lifecycle",
    "## Stage Reconstruction Scope",
    "## Stage Reconstruction Inputs",
    "## Stage Reconstruction Preconditions",
    "## Historical Runtime Stage Set Reference",
    "## Stage Identity Reconstruction",
    "## Stage Version Reconstruction",
    "## Stage Classification Reconstruction",
    "## Stage Lifecycle Reconstruction",
    "## Stage Preconditions Reconstruction",
    "## Stage Inputs Reconstruction",
    "## Stage Outputs Reconstruction",
    "## Stage Entry Reconstruction",
    "## Stage Execution Boundary Reconstruction",
    "## Stage Completion Reconstruction",
    "## Stage Failure Reconstruction",
    "## Stage Cancellation Reconstruction",
    "## Stage Transition Compatibility Reconstruction",
    "## Stage Lifecycle Compatibility Reconstruction",
    "## Stage Ordering Reconstruction",
    "## Stage Binding Reconstruction",
    "## Stage Reconstruction Completeness",
    "## Stage Reconstruction Consistency",
    "## Stage Reconstruction Validation",
    "## Stage Reconstruction Integrity",
    "## Stage Reconstruction Traceability",
    "## Stage Reconstruction Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Stage Reconstruction Invariants",
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
    "STAGE_RECONSTRUCTION_IDENTITY_VIOLATION.",
    "STAGE_RECONSTRUCTION_VERSION_VIOLATION.",
    "STAGE_RECONSTRUCTION_LIFECYCLE_VIOLATION.",
    "STAGE_RECONSTRUCTION_SCOPE_VIOLATION.",
    "STAGE_RECONSTRUCTION_INPUT_VIOLATION.",
    "STAGE_RECONSTRUCTION_PRECONDITION_VIOLATION.",
    "STAGE_RECONSTRUCTION_REFERENCE_VIOLATION.",
    "STAGE_RECONSTRUCTION_BINDING_VIOLATION.",
    "STAGE_RECONSTRUCTION_ORDERING_VIOLATION.",
    "STAGE_RECONSTRUCTION_COMPLETENESS_VIOLATION.",
    "STAGE_RECONSTRUCTION_CONSISTENCY_VIOLATION.",
    "STAGE_RECONSTRUCTION_INTEGRITY_VIOLATION.",
    "STAGE_RECONSTRUCTION_TRACEABILITY_VIOLATION.",
    "STAGE_RECONSTRUCTION_SERIALIZATION_VIOLATION.",
    "STAGE_RECONSTRUCTION_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Stage Reconstruction Identity.",
    "Exactly one Stage Reconstruction Version.",
    "Exactly one Replay Reconstruction.",
    "Exactly one State Reconstruction.",
    "Exactly one Historical Runtime Stage Set.",
    "Exactly one Reconstructed Runtime Stage Set.",
    "Deterministic Stage Ordering.",
    "Complete Stage Bindings.",
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
    assert "Title Commerce Replay Stage Reconstruction Model" in content
    assert "Abbreviation CRStRM" in content
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


def test_normative_dependencies() -> None:
    content = normalized_text()

    for dependency in (
        "CKP-005 Baseline 1.0.",
        "CKP-005 Specification Freeze.",
        "CKP-006 Baseline 1.0.",
        "CKP-006 Specification Freeze.",
        "CKP-007.1 Commerce Reasoning Replay Charter.",
        "CKP-007.2 Replay Structure Model.",
        "CKP-007.3 Replay Request Model.",
        "CKP-007.4 Replay Environment Model.",
        "CKP-007.5 Replay Artifact Resolution Model.",
        "CKP-007.6 Replay Reconstruction Model.",
        "CKP-007.7 Replay State Reconstruction Model.",
    ):
        assert dependency in content


def test_stage_reconstruction_scope() -> None:
    content = normalized_text()

    for requirement in (
        "Historical Runtime Stage Set",
        "Stage Identity Reconstruction",
        "Stage Version Reconstruction",
        "Stage Classification Reconstruction",
        "Stage Lifecycle Reconstruction",
        "Stage Ordering Reconstruction",
        "Stage Binding Reconstruction",
    ):
        assert requirement in content


def test_validation_is_fail_closed() -> None:
    content = normalized_text()

    assert (
        "Stage Reconstruction Validation shall fail closed."
        in content
    )


def test_failure_classifications() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    assert "Stage Reconstruction shall not modify:" in content

    for target in (
        "Historical Runtime Stage Set.",
        "Historical Runtime State.",
        "Historical Runtime Transition Set.",
        "Historical Artifact Set.",
        "Historical Evidence.",
        "Frozen Baselines.",
    ):
        assert target in content


def test_invariants() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_boundary_exclusions() -> None:
    content = normalized_text()

    for excluded in (
        "Replay engine implementation.",
        "Concrete reconstruction algorithms.",
        "Stage implementations.",
        "Schedulers.",
        "Concurrency.",
        "Persistence.",
        "WAL.",
        "Event sourcing.",
        "Distributed infrastructure.",
        "Cryptographic algorithms.",
        "Storage.",
        "Implementation classes.",
    ):
        assert excluded in content


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-007.9" in content
    assert "Replay Transition Reconstruction Model." in content


def test_end_marker() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
