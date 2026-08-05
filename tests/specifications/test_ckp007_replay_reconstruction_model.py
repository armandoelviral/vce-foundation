"""
Executable Specification

CKP-007.6
Commerce Replay Reconstruction Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_RECONSTRUCTION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Reconstruction Identity",
    "## Replay Reconstruction Version",
    "## Replay Reconstruction Lifecycle",
    "## Replay Reconstruction Scope",
    "## Replay Reconstruction Inputs",
    "## Replay Reconstruction Preconditions",
    "## Historical Execution Reconstruction",
    "## Historical Environment Reconstruction",
    "## Historical Artifact Reconstruction",
    "## Runtime State Reconstruction",
    "## Runtime Stage Reconstruction",
    "## Runtime Transition Reconstruction",
    "## Artifact Registry Reconstruction",
    "## Runtime Result Reconstruction",
    "## Reconstruction Ordering",
    "## Reconstruction Completeness",
    "## Reconstruction Consistency",
    "## Reconstruction Validation",
    "## Reconstruction Integrity",
    "## Reconstruction Traceability",
    "## Reconstruction Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Reconstruction Invariants",
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

RECONSTRUCTION_INPUTS = (
    "Replay Request Reference.",
    "Replay Environment Reference.",
    "Artifact Resolution Reference.",
    "Historical Runtime Execution Reference.",
    "Historical Artifact Set.",
    "Resolved Artifact Set.",
)

RECONSTRUCTION_PRECONDITIONS = (
    "Validated Replay Request.",
    "Validated Replay Environment.",
    "Validated Artifact Resolution.",
    "Resolved Historical Artifact Set.",
    "Resolved Historical Runtime Execution.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_RECONSTRUCTION_IDENTITY_VIOLATION.",
    "REPLAY_RECONSTRUCTION_VERSION_VIOLATION.",
    "REPLAY_RECONSTRUCTION_SCOPE_VIOLATION.",
    "REPLAY_RECONSTRUCTION_INPUT_VIOLATION.",
    "REPLAY_RECONSTRUCTION_PRECONDITION_VIOLATION.",
    "REPLAY_RECONSTRUCTION_ORDERING_VIOLATION.",
    "REPLAY_RECONSTRUCTION_COMPLETENESS_VIOLATION.",
    "REPLAY_RECONSTRUCTION_CONSISTENCY_VIOLATION.",
    "REPLAY_RECONSTRUCTION_INTEGRITY_VIOLATION.",
    "REPLAY_RECONSTRUCTION_SERIALIZATION_VIOLATION.",
    "REPLAY_RECONSTRUCTION_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

RECONSTRUCTION_INVARIANTS = (
    "Exactly one Replay Reconstruction Identity.",
    "Exactly one Replay Reconstruction Version.",
    "Exactly one Replay Request.",
    "Exactly one Replay Environment.",
    "Exactly one Artifact Resolution.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Historical Artifact Set.",
    "Exactly one Reconstructed Runtime Result.",
    "Deterministic Ordering.",
    "Integrity Preservation.",
    "Traceability Preservation.",
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

    assert "# CKP-007" in content
    assert "Title Commerce Replay Reconstruction Model" in content
    assert "Abbreviation CRRM" in content
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


def test_no_unexpected_level_two_headings_exist() -> None:
    assert tuple(level_two_headings()) == EXPECTED_SECTIONS


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, and integrity-preserving "
        "Replay Reconstruction.",
        "Replay Reconstruction defines the normative "
        "reconstruction of exactly one historical Runtime Execution.",
        "Replay Reconstruction reconstructs historical execution "
        "exclusively from resolved historical artifacts and pinned "
        "historical environment references.",
        "Replay Reconstruction shall preserve historical equivalence.",
        "This specification defines no Replay engine.",
    ):
        assert requirement in content


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-005 Baseline 1.0.",
        "CKP-005 Specification Freeze.",
        "CKP-006 Baseline 1.0.",
        "CKP-006 Specification Freeze.",
        "CKP-007.1 Commerce Reasoning Replay Charter.",
        "CKP-007.2 Replay Structure Model.",
        "CKP-007.3 Replay Request Model.",
        "CKP-007.4 Replay Environment Model.",
        "CKP-007.5 Replay Artifact Resolution Model.",
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_reconstruction_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Reconstruction shall possess exactly one "
        "immutable Replay Reconstruction Identifier.",
        "CKP-REPLAY-RECONSTRUCTION-000001",
        "Replay Reconstruction Identity shall be globally unique.",
        "Replay Reconstruction Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Reconstruction Identity shall fail validation.",
    ):
        assert requirement in content


def test_reconstruction_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Reconstruction shall declare exactly one Version.",
        "Version identifies the Replay Reconstruction schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_reconstruction_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_reconstruction_scope_is_exactly_one_historical_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Reconstruction shall reconstruct exactly "
        "one Historical Runtime Execution.",
        "Replay Reconstruction shall belong to exactly one "
        "Replay Execution.",
        "Replay Reconstruction Scope shall remain immutable.",
    ):
        assert requirement in content


def test_reconstruction_inputs_are_declared() -> None:
    content = normalized_text()

    for reconstruction_input in RECONSTRUCTION_INPUTS:
        assert reconstruction_input in content

    assert "Every mandatory input shall be present." in content


def test_reconstruction_preconditions_are_declared() -> None:
    content = normalized_text()

    for precondition in RECONSTRUCTION_PRECONDITIONS:
        assert precondition in content

    assert "Every precondition shall succeed." in content


def test_historical_execution_reconstruction_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Historical Runtime Execution.",
        "Historical execution reconstruction shall preserve "
        "historical equivalence.",
    ):
        assert requirement in content


def test_historical_environment_reconstruction_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Historical Runtime Environment.",
        "Historical environment reconstruction shall preserve "
        "pinned historical references.",
    ):
        assert requirement in content


def test_historical_artifact_reconstruction_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Historical Artifact Set.",
        "Historical Artifact Reconstruction shall consume "
        "only resolved artifacts.",
    ):
        assert requirement in content


def test_runtime_state_reconstruction_is_exactly_one_and_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Runtime State.",
        "Runtime State reconstruction shall remain deterministic.",
    ):
        assert requirement in content


def test_runtime_stage_reconstruction_is_exactly_one_and_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Runtime Stage Set.",
        "Runtime Stage reconstruction shall remain deterministic.",
    ):
        assert requirement in content


def test_runtime_transition_reconstruction_is_exactly_one_and_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Runtime Transition Set.",
        "Runtime Transition reconstruction shall remain deterministic.",
    ):
        assert requirement in content


def test_artifact_registry_reconstruction_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Artifact Registry.",
        "Artifact Registry reconstruction shall preserve "
        "historical identities.",
    ):
        assert requirement in content


def test_runtime_result_reconstruction_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall reconstruct exactly one "
        "Runtime Result.",
        "Runtime Result reconstruction shall preserve "
        "historical equivalence.",
    ):
        assert requirement in content


def test_reconstruction_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction shall preserve exactly one "
        "deterministic reconstruction order.",
        "Equivalent Replay executions shall produce equivalent "
        "reconstruction ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_reconstruction_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Every required historical component shall be reconstructed.",
        "Partial reconstruction shall fail validation.",
        "Missing reconstructed components shall fail validation.",
    ):
        assert requirement in content


def test_reconstruction_consistency_is_required() -> None:
    content = normalized_text()

    for property_name in (
        "Identity.",
        "Version.",
        "Ordering.",
        "Integrity.",
        "Traceability.",
    ):
        assert property_name in content

    assert "Consistency violations shall fail validation." in content


def test_reconstruction_validation_is_complete_and_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Inputs.",
        "Preconditions.",
        "Historical reconstruction.",
        "Runtime reconstruction.",
        "Ordering.",
        "Completeness.",
        "Consistency.",
        "Integrity.",
        "Canonical Serialization.",
    ):
        assert validation_check in content

    assert (
        "Replay Reconstruction Validation shall fail closed."
        in content
    )


def test_reconstruction_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "Reconstructed References.",
        "Ordering.",
        "Canonical Serialization.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert (
        "Mutation shall invalidate Replay Reconstruction Integrity."
        in content
    )


def test_reconstruction_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Replay Request.",
        "Replay Environment.",
        "Artifact Resolution.",
        "Historical Runtime Execution.",
        "Historical Artifact Set.",
        "Replay Validation.",
        "Replay Evidence.",
        "Replay Result.",
    ):
        assert traceability_target in content


def test_reconstruction_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Reconstruction belongs to exactly one Replay Execution.",
        "Replay Reconstruction references exactly one Replay Request.",
        "Replay Reconstruction references exactly one "
        "Replay Environment.",
        "Replay Reconstruction references exactly one "
        "Artifact Resolution.",
        "Replay Reconstruction reconstructs exactly one "
        "Historical Runtime Execution.",
        "Replay Reconstruction produces exactly one "
        "Reconstructed Runtime Result.",
        "Relationships shall remain deterministic.",
        "Relationships shall remain resolvable.",
    ):
        assert relationship in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Reconstruction shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "References.",
        "Ordering.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Reconstruction ordering shall be deterministic.",
        "Equivalent Replay Reconstructions shall produce "
        "equivalent ordering.",
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
        "Replay Reconstruction Identity is invalid.",
        "Replay Reconstruction Version is unsupported.",
        "Replay Reconstruction Scope is violated.",
        "Mandatory inputs are missing.",
        "Preconditions are not satisfied.",
        "Historical Runtime Execution cannot be reconstructed.",
        "Historical Artifact Set cannot be reconstructed.",
        "Ordering verification fails.",
        "Completeness verification fails.",
        "Consistency verification fails.",
        "Integrity verification fails.",
        "Canonical serialization fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    for historical_target in (
        "Historical Runtime Execution.",
        "Historical Runtime Environment.",
        "Historical Artifact Set.",
        "Historical Artifact Registry.",
        "Historical Evidence.",
        "Frozen Baselines.",
        "Historical references.",
    ):
        assert historical_target in content

    assert "Replay Reconstruction shall not modify:" in content


def test_reconstruction_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in RECONSTRUCTION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Scope is valid.",
        "Inputs are complete.",
        "Preconditions are satisfied.",
        "Historical Runtime Execution reconstructs.",
        "Historical Artifact Set reconstructs.",
        "Runtime State reconstructs.",
        "Runtime Stage Set reconstructs.",
        "Runtime Transition Set reconstructs.",
        "Artifact Registry reconstructs.",
        "Runtime Result reconstructs.",
        "Integrity is preserved.",
        "Deterministic ordering succeeds.",
        "Validation succeeds.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Reconstruction Identity.",
        "Replay Reconstruction Version.",
        "Replay Reconstruction Lifecycle.",
        "Replay Reconstruction Scope.",
        "Replay Reconstruction Inputs.",
        "Replay Reconstruction Preconditions.",
        "Historical Execution Reconstruction.",
        "Historical Environment Reconstruction.",
        "Historical Artifact Reconstruction.",
        "Runtime State Reconstruction.",
        "Runtime Stage Reconstruction.",
        "Runtime Transition Reconstruction.",
        "Artifact Registry Reconstruction.",
        "Runtime Result Reconstruction.",
        "Reconstruction Ordering.",
        "Reconstruction Completeness.",
        "Reconstruction Consistency.",
        "Reconstruction Validation.",
        "Reconstruction Integrity.",
        "Reconstruction Traceability.",
        "Reconstruction Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Reconstruction Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Concrete reconstruction algorithms.",
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
        assert excluded_capability in content

    assert (
        "Future CKP-007 specifications shall preserve "
        "this Replay Reconstruction Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.7" in content
    assert "Replay State Reconstruction Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
