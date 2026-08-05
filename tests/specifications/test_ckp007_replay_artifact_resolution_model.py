"""
Executable Specification

CKP-007.5
Commerce Replay Artifact Resolution Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_ARTIFACT_RESOLUTION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Artifact Resolution Identity",
    "## Artifact Resolution Version",
    "## Artifact Resolution Lifecycle",
    "## Artifact Resolution Scope",
    "## Artifact Resolution Inputs",
    "## Artifact Resolution Targets",
    "## Artifact Resolution Sources",
    "## Artifact Resolution Ordering",
    "## Artifact Resolution Completeness",
    "## Artifact Resolution Consistency",
    "## Artifact Resolution Validation",
    "## Artifact Resolution Integrity",
    "## Artifact Resolution Traceability",
    "## Artifact Resolution Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Artifact Resolution Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Resolving.",
    "Validated.",
    "Completed.",
    "Archived.",
)

RESOLUTION_INPUTS = (
    "Replay Request Reference.",
    "Replay Environment Reference.",
    "Historical Runtime Execution Reference.",
    "Historical Artifact Registry Reference.",
    "Historical Artifact Set.",
)

RESOLUTION_TARGETS = (
    "Historical Artifact Set.",
    "Resolved Artifact Set.",
    "Artifact Identity.",
    "Artifact Version.",
    "Artifact Type.",
)

RESOLUTION_SOURCES = (
    "Historical Artifact Registry.",
    "Historical Runtime Execution.",
    "Replay Environment.",
    "Replay Request.",
    "Frozen Baselines.",
)

CONSISTENCY_PROPERTIES = (
    "Identity.",
    "Version.",
    "Type.",
    "Integrity.",
    "Traceability.",
)

FAILURE_CLASSIFICATIONS = (
    "ARTIFACT_RESOLUTION_IDENTITY_VIOLATION.",
    "ARTIFACT_RESOLUTION_VERSION_VIOLATION.",
    "ARTIFACT_RESOLUTION_SCOPE_VIOLATION.",
    "ARTIFACT_RESOLUTION_INPUT_VIOLATION.",
    "ARTIFACT_RESOLUTION_SOURCE_VIOLATION.",
    "ARTIFACT_RESOLUTION_ORDERING_VIOLATION.",
    "ARTIFACT_RESOLUTION_COMPLETENESS_VIOLATION.",
    "ARTIFACT_RESOLUTION_CONSISTENCY_VIOLATION.",
    "ARTIFACT_RESOLUTION_INTEGRITY_VIOLATION.",
    "ARTIFACT_RESOLUTION_SERIALIZATION_VIOLATION.",
    "ARTIFACT_RESOLUTION_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

RESOLUTION_INVARIANTS = (
    "Exactly one Artifact Resolution Identity.",
    "Exactly one Artifact Resolution Version.",
    "Exactly one Replay Request.",
    "Exactly one Replay Environment.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Historical Artifact Registry.",
    "Exactly one Historical Artifact Set.",
    "Exactly one Resolved Artifact Set.",
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
    assert (
        "Title Commerce Replay Artifact Resolution Model"
        in content
    )
    assert "Abbreviation CRARM" in content
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
        "Replay Artifact Resolution process.",
        "Replay Artifact Resolution defines the normative "
        "resolution of every historical artifact required "
        "by exactly one Replay.",
        "Replay Artifact Resolution shall resolve historical "
        "artifacts without modifying their historical representation.",
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
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_resolution_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact Resolution shall possess exactly one "
        "immutable Artifact Resolution Identifier.",
        "CKP-ARTIFACT-RESOLUTION-000001",
        "Artifact Resolution Identity shall be globally unique.",
        "Artifact Resolution Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Artifact "
        "Resolution Identity shall fail validation.",
    ):
        assert requirement in content


def test_resolution_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact Resolution shall declare exactly one Version.",
        "Version identifies the Artifact Resolution schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_resolution_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_resolution_scope_is_exactly_one_artifact_set() -> None:
    content = normalized_text()

    for requirement in (
        "One Artifact Resolution shall resolve exactly one "
        "Historical Artifact Set.",
        "Artifact Resolution shall belong to exactly one "
        "Replay Execution.",
        "Artifact Resolution Scope shall remain immutable.",
    ):
        assert requirement in content


def test_resolution_inputs_are_declared() -> None:
    content = normalized_text()

    for resolution_input in RESOLUTION_INPUTS:
        assert resolution_input in content

    assert "Every mandatory input shall be present." in content


def test_resolution_targets_are_declared() -> None:
    content = normalized_text()

    for target in RESOLUTION_TARGETS:
        assert target in content


def test_resolution_sources_are_closed() -> None:
    content = normalized_text()

    for source in RESOLUTION_SOURCES:
        assert source in content

    assert "Unregistered sources shall fail validation." in content


def test_resolution_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Artifact Resolution shall preserve exactly one "
        "deterministic resolution order.",
        "Equivalent Replay executions shall produce equivalent "
        "Artifact Resolution ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_resolution_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Every required historical artifact shall be resolved.",
        "Partial Artifact Resolution shall fail validation.",
        "Missing artifacts shall fail validation.",
    ):
        assert requirement in content


def test_resolution_consistency_is_required() -> None:
    content = normalized_text()

    for property_name in CONSISTENCY_PROPERTIES:
        assert property_name in content

    assert "Consistency violations shall fail validation." in content


def test_resolution_validation_is_complete_and_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Inputs.",
        "Targets.",
        "Sources.",
        "Ordering.",
        "Completeness.",
        "Consistency.",
        "Integrity.",
        "Canonical Serialization.",
    ):
        assert validation_check in content

    assert (
        "Artifact Resolution Validation shall fail closed."
        in content
    )


def test_resolution_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "Resolved References.",
        "Ordering.",
        "Canonical Serialization.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert (
        "Mutation shall invalidate Artifact Resolution Integrity."
        in content
    )


def test_resolution_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Request.",
        "Replay Environment.",
        "Historical Runtime Execution.",
        "Historical Artifact Registry.",
        "Resolved Artifact Set.",
        "Replay Validation.",
        "Replay Result.",
    ):
        assert target in content


def test_resolution_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Artifact Resolution belongs to exactly one Replay Execution.",
        "Artifact Resolution references exactly one Replay Request.",
        "Artifact Resolution references exactly one Replay Environment.",
        "Artifact Resolution references exactly one Historical "
        "Runtime Execution.",
        "Artifact Resolution references exactly one Historical "
        "Artifact Registry.",
        "Artifact Resolution produces exactly one "
        "Resolved Artifact Set.",
        "Relationships shall remain deterministic.",
        "Relationships shall remain resolvable.",
    ):
        assert relationship in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Artifact Resolution shall possess exactly one "
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
        "Artifact Resolution ordering shall be deterministic.",
        "Equivalent Artifact Resolution operations shall "
        "produce equivalent ordering.",
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
        "Artifact Resolution Identity is invalid.",
        "Artifact Resolution Version is unsupported.",
        "Artifact Resolution Scope is violated.",
        "Mandatory inputs are missing.",
        "Historical Artifact Registry cannot be resolved.",
        "Historical Artifact Set cannot be resolved.",
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
        "Historical Artifact Registry.",
        "Historical Runtime Execution.",
        "Historical Artifact Set.",
        "Historical Evidence.",
        "Historical References.",
        "Frozen Baselines.",
    ):
        assert historical_target in content

    assert "Artifact Resolution shall not modify:" in content


def test_resolution_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in RESOLUTION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Scope is valid.",
        "All mandatory inputs exist.",
        "Historical Artifact Registry resolves.",
        "Historical Artifact Set resolves.",
        "Resolved Artifact Set is complete.",
        "Consistency is preserved.",
        "Integrity is preserved.",
        "Deterministic ordering succeeds.",
        "Validation succeeds.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Artifact Resolution Identity.",
        "Artifact Resolution Version.",
        "Artifact Resolution Lifecycle.",
        "Artifact Resolution Scope.",
        "Artifact Resolution Inputs.",
        "Artifact Resolution Targets.",
        "Artifact Resolution Sources.",
        "Artifact Resolution Ordering.",
        "Artifact Resolution Completeness.",
        "Artifact Resolution Consistency.",
        "Artifact Resolution Validation.",
        "Artifact Resolution Integrity.",
        "Artifact Resolution Traceability.",
        "Artifact Resolution Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Artifact Resolution Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Reconstruction algorithms.",
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
        "this Artifact Resolution Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.6" in content
    assert "Replay Reconstruction Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
