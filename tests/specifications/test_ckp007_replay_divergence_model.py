"""
Executable Specification

CKP-007.13
Commerce Replay Divergence Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_DIVERGENCE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Divergence Identity",
    "## Replay Divergence Version",
    "## Replay Divergence Lifecycle",
    "## Replay Divergence Scope",
    "## Replay Divergence Inputs",
    "## Replay Divergence Preconditions",
    "## Replay Comparison Reference",
    "## Divergence Identity",
    "## Divergence Classification",
    "## Divergence Severity",
    "## Divergence Source",
    "## Divergence Target",
    "## Divergence Evidence",
    "## Divergence Context",
    "## Divergence Traceability",
    "## Divergence Integrity",
    "## Divergence Relationships",
    "## Divergence Ordering",
    "## Divergence Resolution Status",
    "## Divergence Validation",
    "## Divergence Completeness",
    "## Divergence Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Divergence Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Recorded.",
    "Validated.",
    "Completed.",
    "Archived.",
)

REQUIRED_INPUTS = (
    "Replay Divergence Identifier.",
    "Replay Divergence Version.",
    "Replay Comparison Reference.",
    "Replay Reconstruction Reference.",
    "Replay Request Reference.",
    "Replay Environment Reference.",
    "Historical Runtime Execution Reference.",
    "Reconstructed Runtime Execution Reference.",
    "Comparison Policy Reference.",
    "Comparison Difference Reference.",
    "Divergence Identifier.",
    "Divergence Classification.",
    "Divergence Severity.",
    "Historical Reference.",
    "Reconstructed Reference.",
    "Compared Property.",
    "Expected Value.",
    "Observed Value.",
    "Divergence Evidence Reference.",
    "Replay Validation Reference.",
    "Replay Evidence Reference.",
    "Replay Result Reference.",
    "Replay Divergence Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Comparison.",
    "Resolved Comparison Difference.",
    "Resolved Comparison Policy.",
    "Resolved Historical Reference.",
    "Resolved Reconstructed Reference.",
    "Verified Historical Integrity.",
    "Verified Reconstructed Integrity.",
    "Verified Comparison Integrity.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_DIVERGENCE_IDENTITY_VIOLATION.",
    "REPLAY_DIVERGENCE_VERSION_VIOLATION.",
    "REPLAY_DIVERGENCE_LIFECYCLE_VIOLATION.",
    "REPLAY_DIVERGENCE_SCOPE_VIOLATION.",
    "REPLAY_DIVERGENCE_INPUT_VIOLATION.",
    "REPLAY_DIVERGENCE_PRECONDITION_VIOLATION.",
    "REPLAY_DIVERGENCE_REFERENCE_VIOLATION.",
    "REPLAY_DIVERGENCE_CLASSIFICATION_VIOLATION.",
    "REPLAY_DIVERGENCE_SEVERITY_VIOLATION.",
    "REPLAY_DIVERGENCE_INTEGRITY_VIOLATION.",
    "REPLAY_DIVERGENCE_TRACEABILITY_VIOLATION.",
    "REPLAY_DIVERGENCE_RELATIONSHIP_VIOLATION.",
    "REPLAY_DIVERGENCE_SERIALIZATION_VIOLATION.",
    "REPLAY_DIVERGENCE_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Replay Divergence Identity.",
    "Exactly one Replay Comparison.",
    "Exactly one Comparison Difference.",
    "Exactly one Divergence Classification.",
    "Exactly one Divergence Severity.",
    "Exactly one Replay Divergence Integrity Reference.",
    "Identity Preservation.",
    "Evidence Preservation.",
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
    assert "Title Commerce Replay Divergence Model" in content
    assert "Abbreviation CRDM" in content
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
        "traceable, and integrity-preserving representation of exactly "
        "one Replay Divergence produced from exactly one Replay Comparison.",
        "Replay Divergence shall represent only explicit Comparison "
        "Differences produced by Replay Comparison.",
        "Replay Divergence shall never introduce, suppress, normalize, "
        "reinterpret, repair, merge, or discard historical or "
        "reconstructed information.",
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
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_replay_divergence_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Divergence shall possess exactly one immutable "
        "Replay Divergence Identifier.",
        "Replay Divergence Identity shall be globally unique.",
        "Replay Divergence Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay Divergence "
        "Identity shall fail validation.",
    ):
        assert requirement in content


def test_replay_divergence_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Divergence shall declare exactly one Version.",
        "Version identifies the Replay Divergence schema.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_replay_divergence_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_replay_divergence_scope_is_exactly_one_difference() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Divergence shall represent exactly one "
        "Comparison Difference.",
        "Replay Divergence shall belong to exactly one Replay Comparison.",
        "Replay Divergence Scope shall remain immutable.",
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


def test_replay_comparison_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence shall reference exactly one immutable "
        "Replay Comparison.",
        "Replay Comparison Reference shall remain resolvable.",
        "Unresolved Replay Comparison Reference shall fail validation.",
    ):
        assert requirement in content


def test_divergence_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Each Replay Divergence shall possess exactly one "
        "Divergence Identifier.",
        "Divergence Identity shall remain immutable.",
        "Duplicate Divergence Identity shall fail validation.",
    ):
        assert requirement in content


def test_divergence_classification_is_explicit() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Divergence shall declare exactly one "
        "Divergence Classification.",
        "Classification shall be explicit.",
        "Classification shall remain immutable.",
        "Unsupported classifications shall fail validation.",
    ):
        assert requirement in content


def test_divergence_severity_is_explicit() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Divergence shall declare exactly one Severity.",
        "Severity shall remain explicit.",
        "Severity shall remain immutable.",
        "Missing Severity shall fail validation.",
    ):
        assert requirement in content


def test_divergence_source_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence shall identify exactly one "
        "Historical Reference.",
        "Replay Divergence shall identify exactly one "
        "Compared Property.",
        "Source information shall remain immutable.",
    ):
        assert requirement in content


def test_divergence_target_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence shall identify exactly one "
        "Reconstructed Reference.",
        "Replay Divergence shall identify exactly one Observed Value.",
        "Target information shall remain immutable.",
    ):
        assert requirement in content


def test_divergence_evidence_is_preserved() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence shall preserve exactly one or more "
        "Divergence Evidence References.",
        "Evidence shall remain immutable.",
        "Evidence shall preserve historical and reconstructed provenance.",
    ):
        assert requirement in content


def test_divergence_context_is_declared() -> None:
    content = normalized_text()

    for context_item in (
        "Comparison Policy Reference.",
        "Historical Context.",
        "Reconstructed Context.",
        "Execution Context.",
    ):
        assert context_item in content

    assert "Context shall remain immutable." in content


def test_divergence_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Comparison.",
        "Replay Reconstruction.",
        "Replay Request.",
        "Replay Environment.",
        "Historical Runtime Execution.",
        "Reconstructed Runtime Execution.",
        "Replay Validation.",
        "Replay Evidence.",
        "Replay Result.",
    ):
        assert target in content

    assert "Traceability shall remain complete." in content


def test_divergence_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Divergence shall possess exactly one deterministic "
        "Replay Divergence Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Comparison Difference.",
        "Historical Reference.",
        "Reconstructed Reference.",
        "Evidence.",
        "Traceability.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Replay Divergence Integrity." in content


def test_divergence_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Divergence belongs to exactly one Replay Comparison.",
        "Replay Divergence references exactly one Comparison Difference.",
        "Replay Divergence references exactly one Replay Reconstruction.",
        "Relationships shall remain explicit.",
        "Relationships shall remain deterministic.",
        "Relationships shall preserve traceability.",
    ):
        assert relationship in content


def test_divergence_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence Ordering shall be deterministic.",
        "Ordering shall follow Comparison Difference ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_divergence_resolution_status_is_non_mutating() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Divergence shall declare exactly one "
        "Resolution Status.",
        "Resolution Status shall describe only divergence disposition.",
        "Resolution Status shall not modify historical evidence.",
        "Resolution Status shall remain immutable.",
    ):
        assert requirement in content


def test_divergence_validation_is_complete_and_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Scope.",
        "Inputs.",
        "Preconditions.",
        "Replay Comparison Reference.",
        "Classification.",
        "Severity.",
        "Source.",
        "Target.",
        "Evidence.",
        "Context.",
        "Integrity.",
        "Traceability.",
        "Relationships.",
        "Ordering.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
    ):
        assert validation_check in content

    assert "Replay Divergence Validation shall fail closed." in content


def test_every_comparison_difference_produces_one_divergence() -> None:
    content = normalized_text()

    for requirement in (
        "Every Comparison Difference shall produce exactly one "
        "Replay Divergence.",
        "Missing Replay Divergence shall fail validation.",
        "Partial Replay Divergence shall fail validation.",
    ):
        assert requirement in content


def test_divergence_consistency_is_declared() -> None:
    content = normalized_text()

    for consistency_target in (
        "Replay Comparison.",
        "Comparison Difference.",
        "Comparison Policy.",
        "Historical Reference.",
        "Reconstructed Reference.",
        "Evidence.",
        "Integrity.",
        "Traceability.",
    ):
        assert consistency_target in content

    assert "Consistency violations shall fail validation." in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Divergence shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Comparison Difference.",
        "Evidence.",
        "Integrity.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Divergence Ordering shall be deterministic.",
        "Equivalent inputs shall produce equivalent ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_central_normative_rules_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Comparison Difference shall produce exactly one "
        "Replay Divergence.",
        "Replay Divergence shall never suppress, reinterpret, "
        "normalize, repair, merge, or discard Comparison Differences.",
        "Replay Divergence shall preserve the original historical evidence.",
        "Replay Divergence shall preserve the reconstructed evidence.",
        "Replay Divergence shall remain immutable.",
        "Replay Divergence shall be deterministic.",
        "Replay Divergence Validation shall fail closed.",
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
        "Replay Comparison cannot be resolved.",
        "Comparison Difference cannot be resolved.",
        "Historical Reference cannot be resolved.",
        "Reconstructed Reference cannot be resolved.",
        "Integrity verification fails.",
        "Traceability is incomplete.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    assert "Replay Divergence shall not modify:" in content

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

    for requirement in (
        "Replay Divergence shall never suppress, reinterpret, "
        "normalize, repair, merge, or discard Comparison Differences.",
        "Replay Divergence shall preserve the original historical evidence.",
        "Replay Divergence shall preserve the reconstructed evidence.",
    ):
        assert requirement in content


def test_replay_divergence_invariants_are_declared() -> None:
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
        "Replay Comparison resolves.",
        "Comparison Difference resolves.",
        "Evidence is complete.",
        "Integrity is preserved.",
        "Traceability is complete.",
        "Relationships resolve.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Divergence Identity.",
        "Replay Divergence Version.",
        "Replay Divergence Lifecycle.",
        "Replay Divergence Scope.",
        "Replay Divergence Inputs.",
        "Replay Divergence Preconditions.",
        "Replay Comparison Reference.",
        "Divergence Identity.",
        "Divergence Classification.",
        "Divergence Severity.",
        "Divergence Source.",
        "Divergence Target.",
        "Divergence Evidence.",
        "Divergence Context.",
        "Divergence Traceability.",
        "Divergence Integrity.",
        "Divergence Relationships.",
        "Divergence Ordering.",
        "Divergence Resolution Status.",
        "Validation.",
        "Completeness.",
        "Consistency.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Divergence Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Resolution algorithms.",
        "Automatic remediation.",
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
        "Replay Divergence Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.14" in content
    assert "Replay Validation Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
