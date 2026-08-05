"""
Executable Specification

CKP-007.2
Commerce Replay Structure Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_STRUCTURE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Structure Identity",
    "## Replay Structure Version",
    "## Replay Structural Scope",
    "## Canonical Replay Structure",
    "## Replay Structural Components",
    "## Replay Instance",
    "## Replay Execution",
    "## Replay Session",
    "## Replay Request Reference",
    "## Historical Execution Reference",
    "## Historical Environment Reference",
    "## Historical Artifact Set",
    "## Resolved Artifact Set",
    "## Reconstructed Environment",
    "## Reconstructed Runtime State",
    "## Reconstructed Stage Set",
    "## Reconstructed Transition Set",
    "## Reconstructed Artifact Registry",
    "## Reconstructed Runtime Result",
    "## Replay Comparison",
    "## Replay Divergence Record",
    "## Replay Evidence",
    "## Replay Validation Reference",
    "## Replay Result",
    "## Structural Relationships",
    "## Cardinality Rules",
    "## Lifecycle Rules",
    "## Structural Integrity",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Structural Validation",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Structural Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

STRUCTURAL_COMPONENTS = (
    "Replay Instance.",
    "Replay Execution.",
    "Replay Session.",
    "Replay Request.",
    "Historical Runtime Execution.",
    "Historical Runtime Result.",
    "Historical Artifact Registry.",
    "Historical Runtime Configuration.",
    "Historical Runtime Limits.",
    "Frozen Baselines.",
    "Historical Artifact Set.",
    "Resolved Artifact Set.",
    "Reconstructed Environment.",
    "Reconstructed Runtime State.",
    "Reconstructed Runtime Stages.",
    "Reconstructed Runtime Transitions.",
    "Reconstructed Artifact Registry.",
    "Reconstructed Runtime Result.",
    "Replay Comparison.",
    "Replay Divergence Record.",
    "Replay Evidence.",
    "Replay Validation Result.",
    "Replay Result.",
)

REPLAY_LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Resolved.",
    "Reconstructed.",
    "Validated.",
    "Completed.",
    "Archived.",
)

CARDINALITY_RULES = (
    "Exactly one Replay Instance.",
    "Exactly one Replay Execution.",
    "Exactly one Replay Session.",
    "Exactly one Replay Request.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Historical Artifact Set.",
    "Exactly one Resolved Artifact Set.",
    "Exactly one Reconstructed Runtime State.",
    "Exactly one Replay Comparison.",
    "Exactly one Replay Result.",
    "Zero or one Replay Divergence Record.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_STRUCTURE_IDENTITY_VIOLATION.",
    "REPLAY_STRUCTURE_VERSION_VIOLATION.",
    "REPLAY_STRUCTURE_SCOPE_VIOLATION.",
    "REPLAY_STRUCTURE_COMPONENT_VIOLATION.",
    "REPLAY_STRUCTURE_RELATIONSHIP_VIOLATION.",
    "REPLAY_STRUCTURE_CARDINALITY_VIOLATION.",
    "REPLAY_STRUCTURE_LIFECYCLE_VIOLATION.",
    "REPLAY_STRUCTURE_INTEGRITY_VIOLATION.",
    "REPLAY_STRUCTURE_SERIALIZATION_VIOLATION.",
    "REPLAY_STRUCTURE_ORDERING_VIOLATION.",
    "STRUCTURAL_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

STRUCTURAL_INVARIANTS = (
    "Exactly one Replay Structure Identity.",
    "Exactly one Replay Structure Version.",
    "Exactly one Replay Instance.",
    "Exactly one Replay Execution.",
    "Exactly one Replay Session.",
    "Exactly one Replay Result.",
    "Deterministic Ordering.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
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
    assert "Title Commerce Replay Structure Model" in content
    assert "Abbreviation CRSM" in content
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


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, replay-compatible, and "
        "integrity-preserving Replay Structure governing "
        "exactly one Replay operation.",
        "The Replay Structure defines the canonical "
        "organization of every Replay.",
        "This specification defines structural identity, "
        "structural scope, structural components, relationships, "
        "lifecycle, integrity, serialization, ordering, validation, "
        "failure semantics, and structural invariants.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define Replay execution.",
        "It does not define reconstruction algorithms.",
        "It does not define persistence.",
        "It does not define WAL.",
        "It does not define event sourcing.",
        "It does not define schedulers.",
        "It does not define concurrency.",
        "It does not define distributed infrastructure.",
        "It does not define cryptographic algorithms.",
        "It does not define storage.",
        "It does not define implementation classes.",
    ):
        assert boundary in content


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
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_structure_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Structure shall possess exactly one "
        "immutable Replay Structure Identifier.",
        "CKP-REPLAY-STRUCTURE-000001",
        "Replay Structure Identity shall be globally unique.",
        "Replay Structure Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Structure Identity shall fail validation.",
    ):
        assert requirement in content


def test_structure_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Structure shall declare exactly one Version.",
        "Version identifies the Replay Structure schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_structural_scope_is_exactly_one_replay() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Structure shall describe exactly one "
        "Replay operation.",
        "Replay Structures shall never span multiple "
        "Replay operations.",
        "Replay Scope shall remain immutable.",
    ):
        assert requirement in content


def test_canonical_replay_structure_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Replay Structure shall contain exactly one "
        "canonical structural representation."
    ) in content

    for preserved_property in (
        "Identity.",
        "Scope.",
        "Relationships.",
        "Ordering.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Canonical Replay Structure shall be deterministic." in content


def test_all_structural_components_are_declared() -> None:
    content = normalized_text()

    for component in STRUCTURAL_COMPONENTS:
        assert component in content

    assert (
        "No additional mandatory structural components shall exist."
    ) in content


def test_replay_instance_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Replay Structure shall contain exactly one "
        "Replay Instance."
    ) in content
    assert "Replay Instance Identity shall remain immutable." in content


def test_replay_execution_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Replay Structure shall contain exactly one "
        "Replay Execution."
    ) in content
    assert (
        "Replay Execution shall belong to exactly one Replay Instance."
    ) in content


def test_replay_session_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Replay Execution shall contain exactly one "
        "Replay Session."
    ) in content
    assert "Replay Session shall remain immutable." in content


def test_replay_request_reference_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall reference exactly one Replay Request."
    ) in content
    assert (
        "Replay Request Reference shall resolve deterministically."
    ) in content


def test_historical_execution_reference_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall reference exactly one "
        "Historical Runtime Execution."
    ) in content
    assert (
        "Historical Execution Reference shall remain immutable."
    ) in content


def test_historical_environment_reference_is_complete() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Structure shall reference exactly one "
        "Historical Runtime Environment.",
        "Historical Runtime Configuration shall be referenced.",
        "Historical Runtime Limits shall be referenced.",
        "Frozen Baselines shall be referenced.",
    ):
        assert requirement in content


def test_historical_artifact_set_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall reference exactly one "
        "Historical Artifact Set."
    ) in content
    assert "Historical Artifact Set shall remain immutable." in content


def test_resolved_artifact_set_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall produce exactly one "
        "Resolved Artifact Set."
    ) in content
    assert (
        "Resolved Artifact Set shall preserve historical identities."
    ) in content


def test_reconstructed_environment_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Environment."
    ) in content
    assert (
        "Environment reconstruction shall remain deterministic."
    ) in content


def test_reconstructed_runtime_state_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Runtime State."
    ) in content
    assert (
        "Runtime State reconstruction shall preserve "
        "historical consistency."
    ) in content


def test_reconstructed_stage_set_is_exactly_one_and_ordered() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Runtime Stage Set."
    ) in content
    assert "Stage ordering shall remain deterministic." in content


def test_reconstructed_transition_set_is_exactly_one_and_ordered() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Runtime Transition Set."
    ) in content
    assert "Transition ordering shall remain deterministic." in content


def test_reconstructed_artifact_registry_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Artifact Registry."
    ) in content
    assert "Artifact Registry shall preserve traceability." in content


def test_reconstructed_runtime_result_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one "
        "Reconstructed Runtime Result."
    ) in content
    assert "Runtime Result shall preserve integrity." in content


def test_replay_comparison_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one Replay Comparison."
    ) in content
    assert (
        "Comparison shall preserve deterministic equivalence."
    ) in content


def test_divergence_record_cardinality_is_zero_or_one() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain zero or one "
        "Replay Divergence Record."
    ) in content
    assert (
        "Replay Divergence Record shall be mandatory only "
        "when divergence exists."
    ) in content


def test_replay_evidence_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one Replay Evidence."
    ) in content
    assert "Replay Evidence shall remain immutable." in content


def test_validation_reference_is_exactly_one_and_fail_closed() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall reference exactly one "
        "Replay Validation Result."
    ) in content
    assert "Replay Validation shall remain fail-closed." in content


def test_replay_result_is_exactly_one_and_terminal() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall contain exactly one Replay Result."
    ) in content
    assert (
        "Replay Result shall represent the terminal Replay outcome."
    ) in content


def test_structural_relationships_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Relationships shall be explicit.",
        "Relationships shall be deterministic.",
        "Relationships shall preserve integrity.",
        "Relationships shall preserve traceability.",
        "Relationships shall be resolvable.",
    ):
        assert requirement in content


def test_cardinality_rules_are_declared() -> None:
    content = normalized_text()

    for rule in CARDINALITY_RULES:
        assert rule in content


def test_lifecycle_rules_are_declared() -> None:
    content = normalized_text()

    for lifecycle_state in REPLAY_LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_structural_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "Relationships.",
        "Ordering.",
        "Serialization.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert (
        "Mutation shall invalidate Structural Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Structure shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Relationships.",
        "Ordering.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Structure ordering shall be deterministic.",
        "Equivalent Replay operations shall produce equivalent "
        "structural ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_structural_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Scope.",
        "Components.",
        "Relationships.",
        "Cardinality.",
        "Lifecycle.",
        "Integrity.",
        "Serialization.",
        "Ordering.",
    ):
        assert validation_check in content

    assert "Structural Validation shall fail closed." in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for failure_condition in (
        "Replay Structure Identity is invalid.",
        "Replay Structure Version is unsupported.",
        "Replay Scope is violated.",
        "Mandatory structural components are missing.",
        "Relationships cannot be resolved.",
        "Cardinality rules are violated.",
        "Lifecycle rules are violated.",
        "Integrity verification fails.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert failure_condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    for historical_artifact in (
        "Historical Runtime Execution.",
        "Historical Runtime Result.",
        "Historical Runtime State.",
        "Historical Artifact Registry.",
        "Historical Evidence.",
        "Historical Facts.",
        "Historical Premises.",
        "Historical Rules.",
        "Frozen Baselines.",
    ):
        assert historical_artifact in content

    assert "Replay Structure shall not modify:" in content


def test_structural_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in STRUCTURAL_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Scope is valid.",
        "All structural components exist.",
        "Relationships resolve.",
        "Cardinality rules are satisfied.",
        "Lifecycle is valid.",
        "Integrity is preserved.",
        "Serialization succeeds.",
        "Deterministic ordering succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Structure Identity.",
        "Replay Structure Version.",
        "Replay Structural Scope.",
        "Canonical Replay Structure.",
        "Replay Structural Components.",
        "Relationships.",
        "Cardinality.",
        "Lifecycle.",
        "Structural Integrity.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Structural Validation.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Structural Invariants.",
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
        "this Structure Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.3" in content
    assert "Replay Request Model." in content
