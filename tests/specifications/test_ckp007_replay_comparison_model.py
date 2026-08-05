"""
Executable Specification

CKP-007.12
Commerce Replay Comparison Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_COMPARISON_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Comparison Identity",
    "## Replay Comparison Version",
    "## Replay Comparison Lifecycle",
    "## Replay Comparison Scope",
    "## Replay Comparison Inputs",
    "## Replay Comparison Preconditions",
    "## Historical Execution Comparison",
    "## Runtime Environment Comparison",
    "## Runtime State Comparison",
    "## Runtime Stage Comparison",
    "## Runtime Transition Comparison",
    "## Artifact Registry Comparison",
    "## Runtime Result Comparison",
    "## Reasoning Status Comparison",
    "## Reasoning Outcome Comparison",
    "## Final Conclusions Comparison",
    "## Proof Reference Comparison",
    "## Reasoning Evidence Comparison",
    "## Runtime Evidence Comparison",
    "## Explanation Comparison",
    "## Validation Result Comparison",
    "## Certification Reference Comparison",
    "## Failure Reference Comparison",
    "## Replay Descriptor Comparison",
    "## Integrity Comparison",
    "## Relationship Comparison",
    "## Comparison Policy",
    "## Comparison Ordering",
    "## Comparison Equivalence",
    "## Comparison Difference",
    "## Comparison Completeness",
    "## Comparison Consistency",
    "## Comparison Validation",
    "## Comparison Integrity",
    "## Comparison Traceability",
    "## Comparison Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Comparison Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Comparing.",
    "Validated.",
    "Completed.",
    "Archived.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_COMPARISON_IDENTITY_VIOLATION.",
    "REPLAY_COMPARISON_VERSION_VIOLATION.",
    "REPLAY_COMPARISON_LIFECYCLE_VIOLATION.",
    "REPLAY_COMPARISON_SCOPE_VIOLATION.",
    "REPLAY_COMPARISON_INPUT_VIOLATION.",
    "REPLAY_COMPARISON_PRECONDITION_VIOLATION.",
    "REPLAY_COMPARISON_TARGET_VIOLATION.",
    "REPLAY_COMPARISON_POLICY_VIOLATION.",
    "REPLAY_COMPARISON_ORDERING_VIOLATION.",
    "REPLAY_COMPARISON_EQUIVALENCE_VIOLATION.",
    "REPLAY_COMPARISON_DIFFERENCE_VIOLATION.",
    "REPLAY_COMPARISON_COMPLETENESS_VIOLATION.",
    "REPLAY_COMPARISON_CONSISTENCY_VIOLATION.",
    "REPLAY_COMPARISON_INTEGRITY_VIOLATION.",
    "REPLAY_COMPARISON_TRACEABILITY_VIOLATION.",
    "REPLAY_COMPARISON_RELATIONSHIP_VIOLATION.",
    "REPLAY_COMPARISON_SERIALIZATION_VIOLATION.",
    "REPLAY_COMPARISON_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

INVARIANTS = (
    "Exactly one Replay Comparison Identity.",
    "Exactly one Replay Comparison Version.",
    "Exactly one Replay Reconstruction.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Reconstructed Runtime Execution.",
    "Exactly one Historical Runtime Environment.",
    "Exactly one Reconstructed Runtime Environment.",
    "Exactly one Historical Runtime State.",
    "Exactly one Reconstructed Runtime State.",
    "Exactly one Historical Runtime Stage Set.",
    "Exactly one Reconstructed Runtime Stage Set.",
    "Exactly one Historical Runtime Transition Set.",
    "Exactly one Reconstructed Runtime Transition Set.",
    "Exactly one Historical Artifact Registry.",
    "Exactly one Reconstructed Artifact Registry.",
    "Exactly one Historical Runtime Result.",
    "Exactly one Reconstructed Runtime Result.",
    "Exactly one Comparison Policy.",
    "Exactly one Comparison Equivalence Result.",
    "Exactly one Comparison Difference Set.",
    "Exactly one Replay Validation.",
    "Exactly one Replay Evidence.",
    "Exactly one Replay Result.",
    "Explicit Difference Preservation.",
    "Comparison Completeness.",
    "Comparison Consistency.",
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
    assert "Title Commerce Replay Comparison Model" in content
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
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, and integrity-preserving "
        "comparison between exactly one Historical Runtime "
        "Execution and exactly one Reconstructed Runtime Execution.",
        "Replay Comparison shall determine whether historical "
        "and reconstructed artifacts are equivalent under exactly "
        "one explicit Comparison Policy.",
        "Replay Comparison shall expose every non-equivalent "
        "property as an explicit Comparison Difference.",
        "Replay Comparison shall not modify, repair, reinterpret, "
        "normalize, suppress, or replace any compared artifact.",
        "This specification defines no Replay engine.",
    ):
        assert requirement in content


def test_normative_dependencies_are_declared() -> None:
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
        "CKP-007.8 Replay Stage Reconstruction Model.",
        "CKP-007.9 Replay Transition Reconstruction Model.",
        "CKP-007.10 Replay Artifact Registry Reconstruction Model.",
        "CKP-007.11 Replay Runtime Result Reconstruction Model.",
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_comparison_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Comparison shall possess exactly one "
        "immutable Replay Comparison Identifier.",
        "CKP-REPLAY-COMPARISON-000001",
        "Replay Comparison Identity shall be globally unique.",
        "Replay Comparison Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Comparison Identity shall fail validation.",
    ):
        assert requirement in content


def test_comparison_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Comparison shall declare exactly one Version.",
        "Version identifies the Replay Comparison schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_comparison_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_comparison_scope_is_exactly_one_pair() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Comparison shall compare exactly one "
        "Historical Runtime Execution with exactly one "
        "Reconstructed Runtime Execution.",
        "Replay Comparison shall belong to exactly one "
        "Replay Reconstruction.",
        "Replay Comparison shall never merge multiple historical "
        "or reconstructed executions.",
        "Replay Comparison Scope shall remain immutable.",
    ):
        assert requirement in content


def test_comparison_policy_is_explicit_and_strict() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Comparison shall reference exactly one immutable "
        "Comparison Policy.",
        "Comparison Policy shall define every property included "
        "in comparison.",
        "Comparison Policy shall define exact equivalence semantics.",
        "Comparison Policy shall not permit implicit tolerances.",
        "Comparison Policy shall not permit implicit normalization.",
        "Comparison Policy shall not permit suppression of "
        "Comparison Differences.",
        "Expected Comparison Policy shall equal the resolved "
        "Comparison Policy.",
        "Comparison Policy mismatch shall fail validation.",
    ):
        assert requirement in content


def test_central_normative_rules_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Equivalent historical and reconstructed artifacts "
        "shall produce an EQUIVALENT comparison result.",
        "Any non-equivalent property shall produce an explicit "
        "comparison difference.",
        "Comparison shall not suppress, reinterpret, repair, "
        "normalize, or tolerate unexplained differences.",
        "Absence of a required comparison target shall fail validation.",
        "Comparison shall be deterministic and fail closed.",
    ):
        assert requirement in content


def test_comparison_domains_are_declared() -> None:
    content = normalized_text()

    for comparison_domain in (
        "Historical Execution Comparison",
        "Runtime Environment Comparison",
        "Runtime State Comparison",
        "Runtime Stage Comparison",
        "Runtime Transition Comparison",
        "Artifact Registry Comparison",
        "Runtime Result Comparison",
        "Reasoning Status Comparison",
        "Reasoning Outcome Comparison",
        "Final Conclusions Comparison",
        "Proof Reference Comparison",
        "Reasoning Evidence Comparison",
        "Runtime Evidence Comparison",
        "Explanation Comparison",
        "Validation Result Comparison",
        "Certification Reference Comparison",
        "Failure Reference Comparison",
        "Replay Descriptor Comparison",
        "Integrity Comparison",
        "Relationship Comparison",
    ):
        assert comparison_domain in content


def test_comparison_equivalence_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Equivalent historical and reconstructed artifacts shall "
        "produce an EQUIVALENT comparison result.",
        "Comparison Equivalence requires every mandatory comparison "
        "target to be equivalent.",
        "Comparison Equivalence shall be deterministic.",
        "An EQUIVALENT result shall contain no Comparison Differences.",
        "Unverified equivalence is prohibited.",
    ):
        assert requirement in content


def test_comparison_difference_is_explicit() -> None:
    content = normalized_text()

    for requirement in (
        "Any non-equivalent property shall produce an explicit "
        "comparison difference.",
        "Comparison target.",
        "Historical value or reference.",
        "Reconstructed value or reference.",
        "Compared property.",
        "Comparison Policy Reference.",
        "Difference classification.",
        "Difference ordering position.",
        "Integrity Reference.",
        "Traceability references.",
        "Comparison Differences shall remain immutable.",
    ):
        assert requirement in content


def test_comparison_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Every mandatory historical and reconstructed target "
        "shall be compared.",
        "Complete execution comparison.",
        "Complete environment comparison.",
        "Complete state comparison.",
        "Complete stage comparison.",
        "Complete transition comparison.",
        "Complete Artifact Registry comparison.",
        "Complete Runtime Result comparison.",
        "Complete evidence comparison.",
        "Complete integrity comparison.",
        "Complete relationship comparison.",
        "Absence of a required comparison target shall fail validation.",
        "Partial comparison shall fail validation.",
    ):
        assert requirement in content


def test_comparison_consistency_is_strict() -> None:
    content = normalized_text()

    for requirement in (
        "An EQUIVALENT result with one or more Comparison "
        "Differences is prohibited.",
        "A non-equivalent result without an explicit Comparison "
        "Difference is prohibited.",
        "Consistency violations shall fail validation.",
    ):
        assert requirement in content


def test_comparison_validation_is_fail_closed() -> None:
    content = normalized_text()

    assert "Comparison shall be deterministic and fail closed." in content
    assert "Comparison Validation shall fail closed." in content


def test_comparison_integrity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Comparison shall possess exactly one deterministic "
        "Replay Comparison Integrity Reference.",
        "Replay Comparison Identity.",
        "Replay Comparison Version.",
        "Comparison Policy Reference.",
        "Historical comparison targets.",
        "Reconstructed comparison targets.",
        "Comparison Ordering.",
        "Comparison Equivalence Result.",
        "Comparison Difference Set.",
        "Canonical Serialization.",
        "Traceability references.",
        "Mutation shall invalidate Comparison Integrity.",
    ):
        assert requirement in content


def test_comparison_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Reconstruction.",
        "State Reconstruction.",
        "Stage Reconstruction.",
        "Transition Reconstruction.",
        "Artifact Registry Reconstruction.",
        "Runtime Result Reconstruction.",
        "Replay Request.",
        "Replay Environment.",
        "Historical Runtime Execution.",
        "Reconstructed Runtime Execution.",
        "Historical Runtime Result.",
        "Reconstructed Runtime Result.",
        "Comparison Policy.",
        "Replay Validation.",
        "Replay Evidence.",
        "Replay Result.",
        "Comparison Difference Set.",
    ):
        assert target in content

    assert "Traceability shall remain complete." in content


def test_comparison_relationships_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Comparison belongs to exactly one Replay Reconstruction.",
        "Replay Comparison references exactly one State Reconstruction.",
        "Replay Comparison references exactly one Stage Reconstruction.",
        "Replay Comparison references exactly one "
        "Transition Reconstruction.",
        "Replay Comparison references exactly one "
        "Artifact Registry Reconstruction.",
        "Replay Comparison references exactly one "
        "Runtime Result Reconstruction.",
        "Replay Comparison references exactly one "
        "Historical Runtime Execution.",
        "Replay Comparison references exactly one "
        "Reconstructed Runtime Execution.",
        "Replay Comparison references exactly one Comparison Policy.",
        "Replay Comparison produces exactly one "
        "Comparison Equivalence Result.",
        "Replay Comparison produces exactly one "
        "Comparison Difference Set.",
        "Relationships shall remain explicit.",
        "Relationships shall remain deterministic.",
        "Relationships shall remain resolvable.",
        "Relationships shall preserve integrity and traceability.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Comparison shall possess exactly one "
        "canonical serialization.",
        "Comparison Policy.",
        "Comparison Ordering.",
        "Comparison Equivalence Result.",
        "Comparison Difference Set.",
        "Integrity.",
        "Traceability.",
        "Canonical serialization shall be deterministic.",
    ):
        assert requirement in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Comparison ordering shall be deterministic.",
        "Comparison Policy shall determine property comparison order.",
        "Comparison Differences shall preserve their canonical "
        "discovery order.",
        "Equivalent Replay Comparison inputs shall produce "
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
        "Replay Comparison Identity is invalid.",
        "Replay Comparison Version is unsupported.",
        "Replay Comparison Lifecycle is invalid.",
        "Replay Comparison Scope is violated.",
        "Mandatory inputs are missing.",
        "Preconditions are not satisfied.",
        "A required historical target cannot be resolved.",
        "A required reconstructed target cannot be resolved.",
        "Comparison Policy cannot be resolved.",
        "Comparison Policy does not match the Expected "
        "Comparison Policy.",
        "Comparison Ordering verification fails.",
        "Equivalence is claimed without complete comparison.",
        "A non-equivalent property lacks an explicit "
        "Comparison Difference.",
        "Comparison Completeness verification fails.",
        "Comparison Consistency verification fails.",
        "Integrity verification fails.",
        "Traceability is incomplete.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    assert "Replay Comparison shall not modify:" in content

    for target in (
        "Historical Runtime Execution.",
        "Historical Runtime Environment.",
        "Historical Runtime State.",
        "Historical Runtime Stage Set.",
        "Historical Runtime Transition Set.",
        "Historical Artifact Registry.",
        "Historical Runtime Result.",
        "Historical Conclusions.",
        "Historical Proof References.",
        "Historical Reasoning Evidence.",
        "Historical Runtime Evidence.",
        "Historical Explanation.",
        "Historical Validation Result.",
        "Historical Certification Reference.",
        "Historical Failure Reference.",
        "Historical Replay Descriptor.",
        "Historical integrity references.",
        "Frozen Baselines.",
        "Historical references.",
    ):
        assert target in content

    assert (
        "Replay Comparison shall not repair, reinterpret, normalize, "
        "suppress, replace, or invent historical artifacts."
    ) in content
    assert "Replay Comparison shall not mutate reconstructed artifacts." in content


def test_comparison_invariants_are_declared() -> None:
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
        "Every historical target resolves.",
        "Every reconstructed target resolves.",
        "Comparison Policy resolves.",
        "Expected Comparison Policy matches.",
        "Every mandatory target is compared.",
        "Comparison Ordering is valid.",
        "Equivalent targets produce an EQUIVALENT result.",
        "Every non-equivalent property produces an explicit "
        "Comparison Difference.",
        "Comparison Completeness is preserved.",
        "Comparison Consistency is preserved.",
        "Validation succeeds.",
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

    for excluded in (
        "Replay engine implementation.",
        "Concrete comparison algorithms.",
        "Implicit numerical tolerances.",
        "Implicit normalization.",
        "Divergence model.",
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
        assert excluded in content

    assert (
        "Future CKP-007 specifications shall preserve this "
        "Replay Comparison Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.13" in content
    assert "Replay Divergence Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
