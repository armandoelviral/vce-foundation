"""
Executable Specification

CKP-007.14
Commerce Replay Validation Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_VALIDATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Validation Identity",
    "## Replay Validation Version",
    "## Replay Validation Lifecycle",
    "## Replay Validation Scope",
    "## Replay Validation Inputs",
    "## Replay Validation Preconditions",
    "## Replay Reconstruction Validation",
    "## Replay Comparison Validation",
    "## Replay Divergence Validation",
    "## Replay Integrity Validation",
    "## Replay Traceability Validation",
    "## Replay Invariant Validation",
    "## Replay Validation Result",
    "## Replay Validation Evidence",
    "## Replay Validation Integrity",
    "## Replay Validation Relationships",
    "## Replay Validation Ordering",
    "## Replay Validation Completeness",
    "## Replay Validation Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Validation Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Validating.",
    "Validated.",
    "Completed.",
    "Archived.",
)

REQUIRED_INPUTS = (
    "Replay Validation Identifier.",
    "Replay Validation Version.",
    "Replay Reconstruction Reference.",
    "Replay Comparison Reference.",
    "Replay Divergence Reference.",
    "Replay Request Reference.",
    "Replay Environment Reference.",
    "Replay Result Reference.",
    "Replay Evidence Reference.",
    "Replay Integrity Reference.",
    "Replay Traceability Reference.",
    "Replay Invariant Reference.",
    "Replay Validation Result.",
    "Replay Validation Evidence.",
    "Replay Validation Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Reconstruction.",
    "Validated Replay Comparison.",
    "Validated Replay Divergence.",
    "Resolved Replay Request.",
    "Resolved Replay Environment.",
    "Resolved Replay Result.",
    "Resolved Replay Evidence.",
    "Verified Replay Integrity.",
    "Verified Replay Traceability.",
    "Verified Replay Invariants.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_VALIDATION_IDENTITY_VIOLATION.",
    "REPLAY_VALIDATION_VERSION_VIOLATION.",
    "REPLAY_VALIDATION_LIFECYCLE_VIOLATION.",
    "REPLAY_VALIDATION_SCOPE_VIOLATION.",
    "REPLAY_VALIDATION_INPUT_VIOLATION.",
    "REPLAY_VALIDATION_PRECONDITION_VIOLATION.",
    "REPLAY_VALIDATION_RECONSTRUCTION_VIOLATION.",
    "REPLAY_VALIDATION_COMPARISON_VIOLATION.",
    "REPLAY_VALIDATION_DIVERGENCE_VIOLATION.",
    "REPLAY_VALIDATION_INTEGRITY_VIOLATION.",
    "REPLAY_VALIDATION_TRACEABILITY_VIOLATION.",
    "REPLAY_VALIDATION_INVARIANT_VIOLATION.",
    "REPLAY_VALIDATION_SERIALIZATION_VIOLATION.",
    "REPLAY_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Replay Validation Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Reconstruction.",
    "Exactly one Replay Comparison.",
    "Exactly one Replay Divergence.",
    "Exactly one Replay Validation Result.",
    "Exactly one Replay Validation Integrity Reference.",
    "Identity Preservation.",
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
    assert "Title Commerce Replay Validation Model" in content
    assert "Abbreviation CRVM" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_required_sections_exist_once() -> None:
    headings = level_two_headings()

    for section in EXPECTED_SECTIONS:
        assert headings.count(section) == 1, section


def test_sections_follow_canonical_order() -> None:
    assert tuple(level_two_headings()) == EXPECTED_SECTIONS


def test_no_duplicate_level_two_headings_exist() -> None:
    headings = level_two_headings()

    assert len(headings) == len(set(headings))


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, fail-closed, "
        "traceable, and integrity-preserving validation of exactly "
        "one Replay.",
        "Replay Validation shall validate the entire Replay as one "
        "normative unit.",
        "Replay Validation shall never modify, reinterpret, normalize, "
        "repair, suppress, or replace any Replay artifact.",
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
        "CKP-007.6 Replay Reconstruction Model.",
        "CKP-007.7 Replay State Reconstruction Model.",
        "CKP-007.8 Replay Stage Reconstruction Model.",
        "CKP-007.9 Replay Transition Reconstruction Model.",
        "CKP-007.10 Replay Artifact Registry Reconstruction Model.",
        "CKP-007.11 Replay Runtime Result Reconstruction Model.",
        "CKP-007.12 Replay Comparison Model.",
        "CKP-007.13 Replay Divergence Model.",
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_replay_validation_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Validation shall possess exactly one immutable "
        "Replay Validation Identifier.",
        "Replay Validation Identity shall be globally unique.",
        "Replay Validation Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay Validation "
        "Identity shall fail validation.",
    ):
        assert requirement in content


def test_replay_validation_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Validation shall declare exactly one Version.",
        "Version identifies the Replay Validation schema.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_replay_validation_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_replay_validation_scope_is_exactly_one_replay() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Validation shall validate exactly one Replay.",
        "Replay Validation shall belong to exactly one Replay.",
        "Replay Validation Scope shall remain immutable.",
    ):
        assert requirement in content


def test_all_mandatory_inputs_are_declared() -> None:
    content = normalized_text()

    for required_input in REQUIRED_INPUTS:
        assert required_input in content

    assert "Every mandatory input shall be present." in content


def test_all_preconditions_are_declared() -> None:
    content = normalized_text()

    for precondition in PRECONDITIONS:
        assert precondition in content

    assert "Every precondition shall succeed." in content


def test_replay_reconstruction_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate exactly one "
        "Replay Reconstruction.",
        "Replay Reconstruction Validation shall preserve "
        "reconstruction integrity.",
        "Replay Reconstruction Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_comparison_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate exactly one Replay Comparison.",
        "Replay Comparison Validation shall preserve comparison integrity.",
        "Replay Comparison Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_divergence_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate exactly one Replay Divergence.",
        "Replay Divergence Validation shall preserve divergence integrity.",
        "Replay Divergence Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_integrity_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate Replay Integrity.",
        "Integrity Validation shall verify the complete "
        "Replay Integrity Reference.",
        "Integrity Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_traceability_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate Replay Traceability.",
        "Traceability shall remain complete.",
        "Traceability Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_invariant_validation_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate Replay Invariants.",
        "Every mandatory invariant shall be validated.",
        "Invariant Validation shall remain immutable.",
    ):
        assert requirement in content


def test_replay_validation_result_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall produce exactly one "
        "Replay Validation Result.",
        "Result shall be explicit.",
        "Result shall remain immutable.",
    ):
        assert requirement in content


def test_replay_validation_evidence_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall produce Replay Validation Evidence.",
        "Evidence shall remain immutable.",
        "Evidence shall preserve complete traceability.",
    ):
        assert requirement in content


def test_replay_validation_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Validation shall possess exactly one deterministic "
        "Replay Validation Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Inputs.",
        "Validation Result.",
        "Evidence.",
        "Traceability.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Replay Validation Integrity." in content


def test_replay_validation_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Validation belongs to exactly one Replay.",
        "Replay Validation references exactly one Replay Reconstruction.",
        "Replay Validation references exactly one Replay Comparison.",
        "Replay Validation references exactly one Replay Divergence.",
        "Relationships shall remain explicit.",
        "Relationships shall remain deterministic.",
        "Relationships shall preserve traceability.",
    ):
        assert relationship in content


def test_replay_validation_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation Ordering shall be deterministic.",
        "Equivalent inputs shall produce equivalent ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_replay_validation_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate all mandatory "
        "Replay components.",
        "Partial validation shall fail validation.",
        "Missing validation targets shall fail validation.",
    ):
        assert requirement in content


def test_replay_validation_consistency_is_declared() -> None:
    content = normalized_text()

    for consistency_target in (
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Divergence.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Replay Invariants.",
    ):
        assert consistency_target in content

    assert "Consistency violations shall fail validation." in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Validation shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Validation Result.",
        "Evidence.",
        "Integrity.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_central_normative_rules_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Validation shall validate exactly one Replay.",
        "Replay Validation shall validate Replay Reconstruction.",
        "Replay Validation shall validate Replay Comparison.",
        "Replay Validation shall validate Replay Divergence.",
        "Replay Validation shall validate Replay Integrity.",
        "Replay Validation shall validate Replay Traceability.",
        "Replay Validation shall validate Replay Invariants.",
        "Replay Validation shall fail closed.",
        "Replay Validation shall be deterministic.",
        "Replay Validation shall remain immutable.",
    ):
        assert requirement in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Identity is invalid.",
        "Version is unsupported.",
        "Mandatory inputs are missing.",
        "Preconditions are not satisfied.",
        "Replay Reconstruction cannot be validated.",
        "Replay Comparison cannot be validated.",
        "Replay Divergence cannot be validated.",
        "Replay Integrity verification fails.",
        "Replay Traceability verification fails.",
        "Replay Invariant verification fails.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    assert "Replay Validation shall not modify:" in content

    for target in (
        "Historical Runtime Execution.",
        "Historical Runtime Environment.",
        "Historical Runtime State.",
        "Historical Runtime Stage Set.",
        "Historical Runtime Transition Set.",
        "Historical Artifact Registry.",
        "Historical Runtime Result.",
        "Historical Evidence.",
        "Historical References.",
        "Frozen Baselines.",
    ):
        assert target in content

    assert (
        "Replay Validation shall never modify, reinterpret, normalize, "
        "repair, suppress, or replace historical artifacts."
    ) in content


def test_replay_validation_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Lifecycle is valid.",
        "Scope is valid.",
        "Inputs are complete.",
        "Preconditions are satisfied.",
        "Replay Reconstruction validates.",
        "Replay Comparison validates.",
        "Replay Divergence validates.",
        "Replay Integrity validates.",
        "Replay Traceability validates.",
        "Replay Invariants validate.",
        "Validation Result is produced.",
        "Integrity is preserved.",
        "Traceability is complete.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Validation Identity.",
        "Replay Validation Version.",
        "Replay Validation Lifecycle.",
        "Replay Validation Scope.",
        "Replay Validation Inputs.",
        "Replay Validation Preconditions.",
        "Replay Reconstruction Validation.",
        "Replay Comparison Validation.",
        "Replay Divergence Validation.",
        "Replay Integrity Validation.",
        "Replay Traceability Validation.",
        "Replay Invariant Validation.",
        "Replay Validation Result.",
        "Replay Validation Evidence.",
        "Replay Validation Integrity.",
        "Replay Validation Relationships.",
        "Replay Validation Ordering.",
        "Replay Validation Completeness.",
        "Replay Validation Consistency.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Validation Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Validation algorithms.",
        "Automatic repair algorithms.",
        "Reasoning algorithms.",
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
        "Future CKP-007 specifications shall preserve this "
        "Replay Validation Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.15" in content
    assert "Replay Certification Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
