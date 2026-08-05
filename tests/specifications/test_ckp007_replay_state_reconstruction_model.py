"""
Executable Specification

CKP-007.7
Commerce Replay State Reconstruction Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_STATE_RECONSTRUCTION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## State Reconstruction Identity",
    "## State Reconstruction Version",
    "## State Reconstruction Lifecycle",
    "## State Reconstruction Scope",
    "## State Reconstruction Inputs",
    "## State Reconstruction Preconditions",
    "## Historical Runtime State Reference",
    "## Initial State Reconstruction",
    "## Intermediate State Reconstruction",
    "## Terminal State Reconstruction",
    "## Working State Reconstruction",
    "## State Snapshot Reconstruction",
    "## Stage Binding Reconstruction",
    "## Transition Binding Reconstruction",
    "## Artifact Reference Reconstruction",
    "## State Evolution Reconstruction",
    "## State Reconstruction Ordering",
    "## State Reconstruction Completeness",
    "## State Reconstruction Consistency",
    "## State Reconstruction Validation",
    "## State Reconstruction Integrity",
    "## State Reconstruction Traceability",
    "## State Reconstruction Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## State Reconstruction Invariants",
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
    "STATE_RECONSTRUCTION_IDENTITY_VIOLATION.",
    "STATE_RECONSTRUCTION_VERSION_VIOLATION.",
    "STATE_RECONSTRUCTION_LIFECYCLE_VIOLATION.",
    "STATE_RECONSTRUCTION_SCOPE_VIOLATION.",
    "STATE_RECONSTRUCTION_INPUT_VIOLATION.",
    "STATE_RECONSTRUCTION_PRECONDITION_VIOLATION.",
    "STATE_RECONSTRUCTION_HISTORICAL_STATE_VIOLATION.",
    "STATE_RECONSTRUCTION_INITIAL_STATE_VIOLATION.",
    "STATE_RECONSTRUCTION_INTERMEDIATE_STATE_VIOLATION.",
    "STATE_RECONSTRUCTION_TERMINAL_STATE_VIOLATION.",
    "STATE_RECONSTRUCTION_WORKING_STATE_VIOLATION.",
    "STATE_RECONSTRUCTION_SNAPSHOT_VIOLATION.",
    "STATE_RECONSTRUCTION_STAGE_BINDING_VIOLATION.",
    "STATE_RECONSTRUCTION_TRANSITION_BINDING_VIOLATION.",
    "STATE_RECONSTRUCTION_ARTIFACT_REFERENCE_VIOLATION.",
    "STATE_RECONSTRUCTION_EVOLUTION_VIOLATION.",
    "STATE_RECONSTRUCTION_ORDERING_VIOLATION.",
    "STATE_RECONSTRUCTION_COMPLETENESS_VIOLATION.",
    "STATE_RECONSTRUCTION_CONSISTENCY_VIOLATION.",
    "STATE_RECONSTRUCTION_INTEGRITY_VIOLATION.",
    "STATE_RECONSTRUCTION_TRACEABILITY_VIOLATION.",
    "STATE_RECONSTRUCTION_RELATIONSHIP_VIOLATION.",
    "STATE_RECONSTRUCTION_SERIALIZATION_VIOLATION.",
    "STATE_RECONSTRUCTION_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one State Reconstruction Identity.",
    "Exactly one State Reconstruction Version.",
    "Exactly one Replay Reconstruction.",
    "Exactly one Replay Request.",
    "Exactly one Replay Environment.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Historical Runtime State.",
    "Exactly one Historical Initial State.",
    "Exactly one Historical Intermediate State Set.",
    "Exactly one Historical Terminal State.",
    "Exactly one Historical Working State.",
    "Exactly one Historical State Snapshot Set.",
    "Exactly one Resolved Artifact Set.",
    "Exactly one Reconstructed Initial State.",
    "Exactly one Reconstructed Intermediate State Set.",
    "Exactly one Reconstructed Terminal State.",
    "Exactly one Reconstructed Working State.",
    "Exactly one Reconstructed State Snapshot Set.",
    "Exactly one Reconstructed Runtime State.",
    "Exactly one Replay Validation.",
    "Exactly one Replay Evidence.",
    "Exactly one Replay Result.",
    "Deterministic State Evolution.",
    "Deterministic Ordering.",
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
    assert "Title Commerce Replay State Reconstruction Model" in content
    assert "Abbreviation CRSRM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_sections_exist_once() -> None:
    hs = headings()

    for section in EXPECTED_SECTIONS:
        assert hs.count(section) == 1


def test_section_order() -> None:
    hs = headings()

    assert tuple(hs) == EXPECTED_SECTIONS


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
    ):
        assert dependency in content


def test_reconstruction_sections_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Initial State Reconstruction",
        "Intermediate State Reconstruction",
        "Terminal State Reconstruction",
        "Working State Reconstruction",
        "State Snapshot Reconstruction",
        "Stage Binding Reconstruction",
        "Transition Binding Reconstruction",
        "Artifact Reference Reconstruction",
        "State Evolution Reconstruction",
    ):
        assert requirement in content


def test_validation_is_fail_closed() -> None:
    content = normalized_text()

    assert (
        "State Reconstruction Validation shall fail closed."
        in content
    )


def test_failure_classifications() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    assert "State Reconstruction shall not modify:" in content

    for target in (
        "Historical Runtime Execution.",
        "Historical Runtime State.",
        "Historical Initial State.",
        "Historical Intermediate State Set.",
        "Historical Terminal State.",
        "Historical Working State.",
        "Historical State Snapshot Set.",
        "Historical Runtime Stage Set.",
        "Historical Runtime Transition Set.",
        "Historical Artifact Registry.",
        "Historical Artifact Set.",
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
        "Concrete state machines.",
        "Comparison algorithms.",
        "Persistence.",
        "WAL.",
        "Event sourcing.",
        "Schedulers.",
        "Concurrency.",
        "Distributed infrastructure.",
        "Cryptographic algorithms.",
        "Storage.",
        "Implementation classes.",
    ):
        assert excluded in content


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-007.8" in content
    assert "Replay Stage Reconstruction Model." in content


def test_end_marker() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
