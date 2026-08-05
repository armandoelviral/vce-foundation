"""
Executable Specification

CKP-007.4
Commerce Replay Environment Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_ENVIRONMENT_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Environment Identity",
    "## Replay Environment Version",
    "## Replay Environment Lifecycle",
    "## Replay Environment Scope",
    "## Historical Runtime Environment",
    "## Historical Runtime Configuration",
    "## Historical Runtime Limits",
    "## Historical Runtime Version",
    "## Historical Runtime Structure Version",
    "## Baseline Pinning",
    "## Registry Pinning",
    "## Environment Compatibility",
    "## Environment Validation",
    "## Environment Integrity",
    "## Environment Traceability",
    "## Environment Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Environment Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Resolved.",
    "Validated.",
    "Pinned.",
    "Used.",
    "Completed.",
    "Archived.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_ENVIRONMENT_IDENTITY_VIOLATION.",
    "REPLAY_ENVIRONMENT_VERSION_VIOLATION.",
    "REPLAY_ENVIRONMENT_SCOPE_VIOLATION.",
    "REPLAY_ENVIRONMENT_REFERENCE_VIOLATION.",
    "REPLAY_ENVIRONMENT_BASELINE_VIOLATION.",
    "REPLAY_ENVIRONMENT_REGISTRY_VIOLATION.",
    "REPLAY_ENVIRONMENT_CONFIGURATION_VIOLATION.",
    "REPLAY_ENVIRONMENT_LIMITS_VIOLATION.",
    "REPLAY_ENVIRONMENT_RUNTIME_VIOLATION.",
    "REPLAY_ENVIRONMENT_STRUCTURE_VERSION_VIOLATION.",
    "REPLAY_ENVIRONMENT_INTEGRITY_VIOLATION.",
    "REPLAY_ENVIRONMENT_SERIALIZATION_VIOLATION.",
    "REPLAY_ENVIRONMENT_ORDERING_VIOLATION.",
    "REPLAY_ENVIRONMENT_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

ENVIRONMENT_INVARIANTS = (
    "Exactly one Replay Environment Identity.",
    "Exactly one Replay Environment Version.",
    "Exactly one Historical Runtime Environment.",
    "Exactly one Historical Runtime Configuration.",
    "Exactly one Historical Runtime Limits.",
    "Exactly one Historical Runtime Version.",
    "Exactly one Historical Runtime Structure Version.",
    "Exactly one Historical Artifact Registry.",
    "Exactly one Replay Request.",
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
    assert "Title Commerce Replay Environment Model" in content
    assert "Abbreviation CREM" in content
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
        "Replay Environment.",
        "Replay Environment defines the complete historical "
        "execution environment required to reconstruct exactly "
        "one historical Runtime Execution.",
        "Replay Environment fixes every normative environmental "
        "dependency required for deterministic Replay.",
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
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_environment_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Environment shall possess exactly one "
        "immutable Replay Environment Identifier.",
        "CKP-REPLAY-ENVIRONMENT-000001",
        "Replay Environment Identity shall be globally unique.",
        "Replay Environment Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Environment Identity shall fail validation.",
    ):
        assert requirement in content


def test_environment_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Environment shall declare exactly one Version.",
        "Version identifies the Replay Environment schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_environment_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_environment_scope_is_exactly_one_historical_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Environment shall describe exactly one "
        "historical Runtime Execution.",
        "Replay Environment shall never span multiple "
        "historical Runtime Executions.",
        "Replay Environment Scope shall remain immutable.",
    ):
        assert requirement in content


def test_historical_runtime_environment_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment shall reference exactly one "
        "Historical Runtime Environment.",
        "Historical Runtime Environment shall remain immutable.",
        "Historical Runtime Environment shall be fully reconstructable.",
    ):
        assert requirement in content


def test_historical_runtime_configuration_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment shall reference exactly one "
        "Historical Runtime Configuration.",
        "Historical Runtime Configuration shall remain immutable.",
        "Configuration mismatch shall fail validation.",
    ):
        assert requirement in content


def test_historical_runtime_limits_are_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment shall reference exactly one "
        "Historical Runtime Limits definition.",
        "Historical Runtime Limits shall remain immutable.",
        "Limits mismatch shall fail validation.",
    ):
        assert requirement in content


def test_historical_runtime_version_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment shall reference exactly one "
        "Historical Runtime Version.",
        "Historical Runtime Version shall remain immutable.",
        "Version mismatch shall fail validation.",
    ):
        assert requirement in content


def test_historical_runtime_structure_version_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment shall reference exactly one "
        "Historical Runtime Structure Version.",
        "Historical Runtime Structure Version shall remain immutable.",
        "Structure Version mismatch shall fail validation.",
    ):
        assert requirement in content


def test_baseline_pinning_is_explicit_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-005 Baseline Reference.",
        "CKP-006 Baseline Reference.",
        "Pinned baselines shall remain immutable.",
        "Baseline mismatch shall fail validation.",
    ):
        assert requirement in content


def test_registry_pinning_is_explicit_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Registry Version References.",
        "Historical Artifact Registry Reference.",
        "Pinned registries shall remain immutable.",
        "Registry mismatch shall fail validation.",
    ):
        assert requirement in content


def test_environment_compatibility_is_declared() -> None:
    content = normalized_text()

    for compatible_reference in (
        "Historical Runtime Version.",
        "Historical Runtime Structure Version.",
        "Pinned Baselines.",
        "Pinned Registries.",
        "Replay Request.",
    ):
        assert compatible_reference in content

    assert "Compatibility shall be deterministic." in content
    assert "Compatibility mismatch shall fail validation." in content


def test_environment_validation_is_complete_and_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Scope.",
        "Historical Runtime Environment.",
        "Historical Runtime Configuration.",
        "Historical Runtime Limits.",
        "Historical Runtime Version.",
        "Historical Runtime Structure Version.",
        "Pinned Baselines.",
        "Pinned Registries.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
    ):
        assert validation_check in content

    assert "Replay Environment Validation shall fail closed." in content


def test_environment_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "References.",
        "Pinned Versions.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert (
        "Mutation shall invalidate Replay Environment Integrity."
        in content
    )


def test_environment_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Historical Runtime Execution.",
        "Historical Artifact Registry.",
        "Replay Request.",
        "Replay Validation.",
        "Replay Result.",
        "Frozen Baselines.",
    ):
        assert traceability_target in content


def test_environment_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Environment belongs to exactly one Replay Instance.",
        "Replay Environment belongs to exactly one Replay Execution.",
        "Replay Environment is referenced by exactly one "
        "Replay Request.",
        "Replay Environment references exactly one Historical "
        "Runtime Execution.",
        "Replay Environment references exactly one Historical "
        "Artifact Registry.",
        "Replay Environment references exactly one Replay Validation.",
        "Relationships shall remain deterministic.",
        "Relationships shall remain resolvable.",
    ):
        assert relationship in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Environment shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "References.",
        "Pinned Versions.",
        "Ordering.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Environment ordering shall be deterministic.",
        "Equivalent Replay Environments shall produce "
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
        "Replay Environment Identity is invalid.",
        "Replay Environment Version is unsupported.",
        "Replay Environment Scope is violated.",
        "Historical Runtime Environment cannot be resolved.",
        "Historical Runtime Configuration cannot be resolved.",
        "Historical Runtime Limits cannot be resolved.",
        "Historical Runtime Version cannot be resolved.",
        "Historical Runtime Structure Version cannot be resolved.",
        "Baseline pinning fails.",
        "Registry pinning fails.",
        "Integrity verification fails.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    for historical_target in (
        "Historical Runtime Environment.",
        "Historical Runtime Configuration.",
        "Historical Runtime Limits.",
        "Historical Runtime Version.",
        "Historical Runtime Structure Version.",
        "Historical Artifact Registry.",
        "Historical Runtime Execution.",
        "Frozen Baselines.",
        "Historical references.",
    ):
        assert historical_target in content

    assert "Replay Environment shall not modify:" in content


def test_environment_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in ENVIRONMENT_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Scope is valid.",
        "Historical Runtime Environment resolves.",
        "Historical Runtime Configuration resolves.",
        "Historical Runtime Limits resolve.",
        "Historical Runtime Version resolves.",
        "Historical Runtime Structure Version resolves.",
        "Pinned Baselines resolve.",
        "Pinned Registries resolve.",
        "Integrity is preserved.",
        "Deterministic ordering succeeds.",
        "Validation succeeds.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Environment Identity.",
        "Replay Environment Version.",
        "Replay Environment Lifecycle.",
        "Replay Environment Scope.",
        "Historical Runtime Environment.",
        "Historical Runtime Configuration.",
        "Historical Runtime Limits.",
        "Historical Runtime Version.",
        "Historical Runtime Structure Version.",
        "Baseline Pinning.",
        "Registry Pinning.",
        "Environment Compatibility.",
        "Environment Validation.",
        "Environment Integrity.",
        "Environment Traceability.",
        "Environment Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Environment Invariants.",
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
        "this Replay Environment Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.5" in content
    assert "Replay Artifact Resolution Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
