"""
Executable Specification

CKP-007.15
Commerce Replay Certification Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_CERTIFICATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Certification Identity",
    "## Replay Certification Version",
    "## Replay Certification Lifecycle",
    "## Replay Certification Scope",
    "## Replay Certification Inputs",
    "## Replay Certification Preconditions",
    "## Replay Validation Reference",
    "## Replay Certification Decision",
    "## Certification Status",
    "## Certification Basis",
    "## Certification Evidence",
    "## Certification Integrity",
    "## Certification Traceability",
    "## Certification Relationships",
    "## Certification Ordering",
    "## Certification Completeness",
    "## Certification Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Certification Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Certifying.",
    "Certified.",
    "Archived.",
)

CERTIFICATION_STATUSES = (
    "Pending.",
    "Certified.",
    "Rejected.",
)

REQUIRED_INPUTS = (
    "Replay Certification Identifier.",
    "Replay Certification Version.",
    "Replay Validation Reference.",
    "Replay Reconstruction Reference.",
    "Replay Comparison Reference.",
    "Replay Divergence Reference.",
    "Replay Result Reference.",
    "Replay Validation Result Reference.",
    "Replay Evidence Reference.",
    "Certification Decision.",
    "Certification Status.",
    "Certification Basis.",
    "Certification Evidence Reference.",
    "Replay Certification Integrity Reference.",
    "Replay Certification Traceability Reference.",
)

PRECONDITIONS = (
    "Validated Replay Validation.",
    "Validated Replay Reconstruction.",
    "Validated Replay Comparison.",
    "Validated Replay Divergence.",
    "Resolved Replay Result.",
    "Resolved Replay Evidence.",
    "Verified Replay Integrity.",
    "Verified Replay Traceability.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_CERTIFICATION_IDENTITY_VIOLATION.",
    "REPLAY_CERTIFICATION_VERSION_VIOLATION.",
    "REPLAY_CERTIFICATION_LIFECYCLE_VIOLATION.",
    "REPLAY_CERTIFICATION_SCOPE_VIOLATION.",
    "REPLAY_CERTIFICATION_INPUT_VIOLATION.",
    "REPLAY_CERTIFICATION_PRECONDITION_VIOLATION.",
    "REPLAY_CERTIFICATION_VALIDATION_VIOLATION.",
    "REPLAY_CERTIFICATION_INTEGRITY_VIOLATION.",
    "REPLAY_CERTIFICATION_TRACEABILITY_VIOLATION.",
    "REPLAY_CERTIFICATION_SERIALIZATION_VIOLATION.",
    "REPLAY_CERTIFICATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Replay Certification Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Validation.",
    "Exactly one Certification Decision.",
    "Exactly one Certification Status.",
    "Exactly one Replay Certification Integrity Reference.",
    "Identity Preservation.",
    "Validation Preservation.",
    "Evidence Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Certification.",
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
    assert "Title Commerce Replay Certification Model" in content
    assert "Abbreviation CRCM" in content
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
        "traceable, and integrity-preserving certification of exactly "
        "one validated Replay.",
        "Replay Certification shall represent the final normative "
        "decision of the Replay pipeline.",
        "Replay Certification shall never modify, reinterpret, normalize, "
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
        "CKP-007.14 Replay Validation Model.",
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_certification_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Certification shall possess exactly one immutable "
        "Replay Certification Identifier.",
        "Replay Certification Identity shall be globally unique.",
        "Replay Certification Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay Certification "
        "Identity shall fail validation.",
    ):
        assert requirement in content


def test_certification_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Certification shall declare exactly one Version.",
        "Version identifies the Replay Certification schema.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_certification_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_certification_scope_is_exactly_one_replay() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Certification shall certify exactly one Replay.",
        "Replay Certification shall belong to exactly one Replay.",
        "Replay Certification Scope shall remain immutable.",
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


def test_replay_validation_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall reference exactly one immutable "
        "Replay Validation.",
        "Replay Validation Reference shall remain resolvable.",
        "Unresolved Replay Validation Reference shall fail validation.",
    ):
        assert requirement in content


def test_certification_decision_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall produce exactly one "
        "Certification Decision.",
        "Certification Decision shall remain explicit.",
        "Certification Decision shall remain immutable.",
    ):
        assert requirement in content


def test_certification_status_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Certification shall declare exactly one "
        "Certification Status."
    ) in content

    for status in CERTIFICATION_STATUSES:
        assert status in content

    assert "Unsupported Certification Status shall fail validation." in content


def test_certification_basis_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall preserve exactly one "
        "Certification Basis.",
        "Certification Basis shall reference the validated Replay.",
        "Certification Basis shall remain immutable.",
    ):
        assert requirement in content


def test_certification_evidence_is_preserved() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall preserve Certification Evidence.",
        "Certification Evidence shall remain immutable.",
        "Certification Evidence shall preserve complete traceability.",
    ):
        assert requirement in content


def test_certification_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Certification shall possess exactly one deterministic "
        "Replay Certification Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Certification Decision.",
        "Certification Status.",
        "Evidence.",
        "Traceability.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Replay Certification Integrity." in content


def test_certification_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Replay Validation.",
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Divergence.",
        "Replay Result.",
        "Replay Evidence.",
        "Replay Integrity.",
    ):
        assert traceability_target in content

    assert "Traceability shall remain complete." in content


def test_certification_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Certification belongs to exactly one Replay.",
        "Replay Certification references exactly one Replay Validation.",
        "Replay Certification references exactly one Replay Result.",
        "Replay Certification references exactly one Replay Evidence.",
        "Relationships shall remain explicit.",
        "Relationships shall remain deterministic.",
        "Relationships shall preserve traceability.",
    ):
        assert relationship in content


def test_certification_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification Ordering shall be deterministic.",
        "Equivalent inputs shall produce equivalent ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_certification_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall certify all mandatory "
        "Replay components.",
        "Partial certification shall fail validation.",
        "Missing certification targets shall fail validation.",
    ):
        assert requirement in content


def test_certification_consistency_is_declared() -> None:
    content = normalized_text()

    for consistency_target in (
        "Replay Validation.",
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Divergence.",
        "Replay Integrity.",
        "Replay Traceability.",
    ):
        assert consistency_target in content

    assert "Consistency violations shall fail validation." in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Certification shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Certification Decision.",
        "Evidence.",
        "Integrity.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent ordering.",
        "Implementation-defined ordering is prohibited.",
    ):
        assert requirement in content


def test_central_normative_rules_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Certification shall certify exactly one Replay.",
        "Replay Certification shall require exactly one successful "
        "Replay Validation.",
        "Replay Certification shall produce exactly one "
        "Certification Decision.",
        "Replay Certification shall preserve Replay Validation.",
        "Replay Certification shall preserve Replay Evidence.",
        "Replay Certification shall preserve Replay Integrity.",
        "Replay Certification shall preserve Replay Traceability.",
        "Replay Certification shall be deterministic.",
        "Replay Certification shall remain immutable.",
        "Replay Certification shall fail closed.",
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
        "Replay Validation cannot be resolved.",
        "Replay Integrity verification fails.",
        "Replay Traceability verification fails.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    assert "Replay Certification shall not modify:" in content

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
        "Replay Certification shall never modify, reinterpret, normalize, "
        "repair, suppress, or replace historical artifacts."
    ) in content


def test_certification_invariants_are_declared() -> None:
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
        "Replay Validation resolves.",
        "Certification Decision exists.",
        "Certification Status exists.",
        "Evidence is complete.",
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
        "Replay Certification Identity.",
        "Replay Certification Version.",
        "Replay Certification Lifecycle.",
        "Replay Certification Scope.",
        "Replay Certification Inputs.",
        "Replay Certification Preconditions.",
        "Replay Validation Reference.",
        "Certification Decision.",
        "Certification Status.",
        "Certification Basis.",
        "Certification Evidence.",
        "Certification Integrity.",
        "Certification Traceability.",
        "Certification Relationships.",
        "Certification Ordering.",
        "Certification Completeness.",
        "Certification Consistency.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Certification Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Certification engine.",
        "PKI.",
        "X.509.",
        "Digital signatures.",
        "Cryptographic algorithms.",
        "Persistence.",
        "WAL.",
        "Event sourcing.",
        "Schedulers.",
        "Concurrency.",
        "Distributed infrastructure.",
        "Storage.",
        "Implementation classes.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-007 specifications shall preserve this "
        "Replay Certification Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.16" in content
    assert "Replay Evidence Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
