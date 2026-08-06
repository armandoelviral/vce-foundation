"""
Executable Specification

CKP-007.21
Commerce Replay Consistency Audit Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_CONSISTENCY_AUDIT_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Consistency Audit Identity",
    "## Replay Consistency Audit Version",
    "## Replay Consistency Audit Lifecycle",
    "## Replay Consistency Audit Scope",
    "## Replay Consistency Audit Inputs",
    "## Replay Consistency Audit Preconditions",
    "## Replay Archive Reference",
    "## Replay Result Reference",
    "## Replay Failure Reference",
    "## Replay Attestation Reference",
    "## Replay Evidence Reference",
    "## Replay Certification Reference",
    "## Replay Validation Reference",
    "## Replay Comparison Reference",
    "## Replay Reconstruction Reference",
    "## Audit Identity",
    "## Audit Status",
    "## Audit Scope",
    "## Consistency Rules",
    "## Consistency Findings",
    "## Audit Integrity",
    "## Audit Traceability",
    "## Audit Relationships",
    "## Audit Ordering",
    "## Audit Completeness",
    "## Audit Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Consistency Audit Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Audited.",
    "Archived.",
)

AUDIT_STATUSES = (
    "CONSISTENT.",
    "INCONSISTENT.",
    "FAILED.",
)

REQUIRED_INPUTS = (
    "Replay Consistency Audit Identifier.",
    "Replay Consistency Audit Version.",
    "Replay Archive Reference.",
    "Replay Result Reference.",
    "Replay Failure Reference.",
    "Replay Attestation Reference.",
    "Replay Evidence Reference.",
    "Replay Certification Reference.",
    "Replay Validation Reference.",
    "Replay Comparison Reference.",
    "Replay Reconstruction Reference.",
    "Audit Identifier.",
    "Audit Status.",
    "Audit Scope.",
    "Consistency Rules.",
    "Consistency Findings.",
    "Audit Integrity Reference.",
    "Audit Traceability Reference.",
    "Replay Consistency Audit Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Archive.",
    "Validated Replay Result.",
    "Validated Replay Validation.",
    "Validated Replay Comparison.",
    "Validated Replay Reconstruction.",
    "Resolved Replay Integrity.",
    "Resolved Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Consistency Audit shall preserve exactly one Replay.",
    "Replay Consistency Audit shall require exactly one Replay Archive.",
    "Replay Consistency Audit shall verify Replay Result.",
    "Replay Consistency Audit shall verify Replay Failure when present.",
    "Replay Consistency Audit shall verify Replay Attestation when present.",
    "Replay Consistency Audit shall verify Replay Evidence when present.",
    "Replay Consistency Audit shall verify Replay Certification when present.",
    "Replay Consistency Audit shall verify Replay Validation.",
    "Replay Consistency Audit shall verify Replay Comparison.",
    "Replay Consistency Audit shall verify Replay Reconstruction.",
    "Replay Consistency Audit shall preserve Replay Integrity.",
    "Replay Consistency Audit shall preserve Replay Traceability.",
    "Replay Consistency Audit shall be deterministic.",
    "Replay Consistency Audit shall remain immutable.",
    "Replay Consistency Audit shall fail closed.",
)

CONSISTENCY_RULES = (
    "Identity uniqueness.",
    "Version compatibility.",
    "Lifecycle compatibility.",
    "Status compatibility.",
    "Outcome compatibility.",
    "Reference resolution.",
    "Relationship consistency.",
    "Cardinality preservation.",
    "Integrity preservation.",
    "Traceability preservation.",
    "Canonical serialization.",
    "Deterministic ordering.",
    "Read-only historical preservation.",
    "Fail-closed semantics.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_CONSISTENCY_AUDIT_IDENTITY_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_VERSION_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_LIFECYCLE_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_SCOPE_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_INPUT_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_PRECONDITION_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_REFERENCE_VIOLATION.",
    "AUDIT_IDENTITY_VIOLATION.",
    "AUDIT_STATUS_VIOLATION.",
    "AUDIT_SCOPE_VIOLATION.",
    "CONSISTENCY_RULES_VIOLATION.",
    "CONSISTENCY_FINDINGS_VIOLATION.",
    "AUDIT_INTEGRITY_VIOLATION.",
    "AUDIT_TRACEABILITY_VIOLATION.",
    "AUDIT_RELATIONSHIP_VIOLATION.",
    "AUDIT_ORDERING_VIOLATION.",
    "AUDIT_COMPLETENESS_VIOLATION.",
    "AUDIT_CONSISTENCY_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_SERIALIZATION_VIOLATION.",
    "REPLAY_CONSISTENCY_AUDIT_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Consistency Audit Identity is invalid.",
    "Replay Consistency Audit Version is unsupported.",
    "Mandatory inputs are missing.",
    "Mandatory references cannot be resolved.",
    "Replay Archive cannot be resolved.",
    "Replay Result cannot be resolved.",
    "Replay Validation cannot be resolved.",
    "Replay Comparison cannot be resolved.",
    "Replay Reconstruction cannot be resolved.",
    "Required conditional references cannot be resolved.",
    "Audit Status is invalid.",
    "Audit Scope is incomplete.",
    "Consistency Rules are incomplete.",
    "Consistency Findings are incomplete.",
    "Audit Integrity verification fails.",
    "Audit Traceability verification fails.",
    "Canonical serialization fails.",
    "Deterministic ordering fails.",
    "Any mandatory invariant is violated.",
)

READ_ONLY_TARGETS = (
    "Historical Runtime Execution.",
    "Historical Runtime Environment.",
    "Historical Runtime State.",
    "Historical Runtime Stage Set.",
    "Historical Runtime Transition Set.",
    "Historical Artifact Registry.",
    "Historical Runtime Result.",
    "Historical Replay Reconstruction.",
    "Historical Replay Comparison.",
    "Historical Replay Validation.",
    "Historical Replay Certification.",
    "Historical Replay Evidence.",
    "Historical Replay Attestation.",
    "Historical Replay Failure.",
    "Historical Replay Result.",
    "Historical Replay Archive.",
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Consistency Audit Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Archive.",
    "Exactly one Replay Result.",
    "Exactly one Audit Status.",
    "Exactly one Audit Scope.",
    "Exactly one Consistency Rules set.",
    "Exactly one Consistency Findings set.",
    "Exactly one Replay Consistency Audit Integrity Reference.",
    "Identity Preservation.",
    "Archive Preservation.",
    "Result Preservation.",
    "Consistency Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Audit.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Archive resolves successfully.",
    "Replay Result resolves successfully.",
    "Replay Validation resolves successfully.",
    "Replay Comparison resolves successfully.",
    "Replay Reconstruction resolves successfully.",
    "All required conditional references resolve successfully.",
    "Audit Status is valid.",
    "Audit Scope is complete.",
    "Consistency Rules are complete.",
    "Consistency Findings are complete.",
    "Audit Integrity is verified.",
    "Audit Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Consistency Audit Identity.",
    "Replay Consistency Audit Version.",
    "Replay Consistency Audit Lifecycle.",
    "Replay Consistency Audit Scope.",
    "Replay Consistency Audit Inputs.",
    "Replay Consistency Audit Preconditions.",
    "Replay Archive Reference.",
    "Replay Result Reference.",
    "Replay Failure Reference.",
    "Replay Attestation Reference.",
    "Replay Evidence Reference.",
    "Replay Certification Reference.",
    "Replay Validation Reference.",
    "Replay Comparison Reference.",
    "Replay Reconstruction Reference.",
    "Audit Identity.",
    "Audit Status.",
    "Audit Scope.",
    "Consistency Rules.",
    "Consistency Findings.",
    "Audit Integrity.",
    "Audit Traceability.",
    "Audit Relationships.",
    "Audit Ordering.",
    "Audit Completeness.",
    "Audit Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Consistency Audit Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Audit engine.",
    "Consistency algorithms.",
    "Remediation engine.",
    "Repair engine.",
    "Archive engine.",
    "Storage engine.",
    "Persistence.",
    "WAL.",
    "Event sourcing.",
    "Scheduler.",
    "Concurrency.",
    "Distributed infrastructure.",
    "Cryptographic algorithms.",
    "PKI.",
    "HSM.",
    "Implementation classes.",
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
    assert "Title Commerce Replay Consistency Audit Model" in content
    assert "Abbreviation CRCAM" in content
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


def test_lifecycle_states_are_exact() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content
    assert "No additional lifecycle states shall be defined" in content


def test_audit_statuses_are_exact() -> None:
    content = normalized_text()

    assert (
        "Every Replay Consistency Audit shall declare exactly one Audit Status."
        in content
    )

    for status in AUDIT_STATUSES:
        assert status in content

    assert "Unsupported Audit Status shall fail validation." in content
    assert (
        "Replay Consistency Audit Lifecycle and Audit Status shall remain "
        "independent normative concepts."
    ) in content


def test_all_required_inputs_are_declared() -> None:
    content = normalized_text()

    for required_input in REQUIRED_INPUTS:
        assert required_input in content

    assert "Every mandatory input shall be present." in content
    assert "Missing mandatory inputs shall fail validation." in content


def test_all_preconditions_are_declared() -> None:
    content = normalized_text()

    for precondition in PRECONDITIONS:
        assert precondition in content

    assert "Every precondition shall succeed." in content
    assert "Unsatisfied preconditions shall fail validation." in content


def test_central_normative_rules_are_declared() -> None:
    content = normalized_text()

    for rule in CENTRAL_RULES:
        assert rule in content


def test_replay_archive_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall reference exactly one immutable "
        "Replay Archive.",
        "Replay Archive Reference shall remain resolvable.",
        "Replay Archive Reference shall remain immutable.",
        "Replay Archive Reference shall preserve complete traceability.",
        "Missing Replay Archive Reference shall fail validation.",
        "Unresolved Replay Archive Reference shall fail validation.",
    ):
        assert requirement in content


def test_replay_result_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall reference exactly one immutable "
        "Replay Result.",
        "Replay Result Reference shall remain resolvable.",
        "Replay Result Reference shall remain immutable.",
        "Replay Result Reference shall preserve complete traceability.",
        "Missing Replay Result Reference shall fail validation.",
    ):
        assert requirement in content


def test_conditional_references_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall reference exactly one "
        "Replay Failure when present in the Replay Archive.",
        "Replay Consistency Audit shall reference exactly one "
        "Replay Attestation when present in the Replay Archive.",
        "Replay Consistency Audit shall reference exactly one "
        "Replay Evidence when present in the Replay Archive.",
        "Replay Consistency Audit shall reference exactly one "
        "Replay Certification when present in the Replay Archive.",
    ):
        assert requirement in content


def test_mandatory_replay_references_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall reference exactly one immutable "
        "Replay Validation.",
        "Replay Consistency Audit shall reference exactly one immutable "
        "Replay Comparison.",
        "Replay Consistency Audit shall reference exactly one immutable "
        "Replay Reconstruction.",
    ):
        assert requirement in content


def test_audit_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Audit shall possess exactly one immutable Audit Identifier.",
        "Audit Identity shall be globally unique.",
        "Audit Identity shall never be reused.",
        "Missing Audit Identifier shall fail validation.",
        "Malformed Audit Identifier shall fail validation.",
        "Duplicated Audit Identifier shall fail validation.",
    ):
        assert requirement in content


def test_audit_scope_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall declare exactly one Audit Scope.",
        "Audit Scope shall identify the complete normative Replay "
        "artifact set subject to the audit.",
        "Audit Scope shall remain immutable.",
        "Audit Scope shall remain fully traceable.",
        "Missing Audit Scope shall fail validation.",
        "Incomplete Audit Scope shall fail validation.",
    ):
        assert requirement in content


def test_audit_scope_contains_required_targets() -> None:
    content = normalized_text()

    for target in (
        "Replay Archive.",
        "Replay Result.",
        "Replay Validation.",
        "Replay Comparison.",
        "Replay Reconstruction.",
        "Replay Failure when present.",
        "Replay Attestation when present.",
        "Replay Evidence when present.",
        "Replay Certification when present.",
    ):
        assert target in content


def test_consistency_rules_are_complete() -> None:
    content = normalized_text()

    assert (
        "Replay Consistency Audit shall declare exactly one complete "
        "Consistency Rules set."
    ) in content

    for rule in CONSISTENCY_RULES:
        assert rule in content

    assert "Consistency Rules shall remain immutable." in content
    assert "Incomplete Consistency Rules shall fail validation." in content


def test_consistency_findings_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall produce exactly one "
        "Consistency Findings set.",
        "Consistency Findings shall preserve every identified "
        "consistency result.",
        "Consistency Findings shall declare all detected "
        "inconsistencies explicitly.",
        "Consistency Findings shall not suppress, normalize, reinterpret, "
        "repair, merge, or discard audit findings.",
        "Consistency Findings shall remain immutable.",
        "Consistency Findings shall remain completely traceable.",
        "Missing Consistency Findings shall fail validation.",
        "Incomplete Consistency Findings shall fail validation.",
    ):
        assert requirement in content


def test_audit_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Consistency Audit shall possess exactly one deterministic "
        "Audit Integrity Reference."
    ) in content

    for binding in (
        "Replay Consistency Audit Identity.",
        "Replay Consistency Audit Version.",
        "Audit Identity.",
        "Audit Status.",
        "Audit Scope.",
        "Consistency Rules.",
        "Consistency Findings.",
        "Audit Traceability.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Audit Integrity." in content
    assert "Audit Integrity shall remain immutable." in content


def test_audit_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Archive.",
        "Replay Result.",
        "Replay Failure when present.",
        "Replay Attestation when present.",
        "Replay Evidence when present.",
        "Replay Certification when present.",
        "Replay Validation.",
        "Replay Comparison.",
        "Replay Reconstruction.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Consistency Rules.",
        "Consistency Findings.",
    ):
        assert target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_audit_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Consistency Audit belongs to exactly one Replay.",
        "Replay Consistency Audit references exactly one Replay Archive.",
        "Replay Consistency Audit references exactly one Replay Result.",
        "Replay Consistency Audit references exactly one Replay Validation.",
        "Replay Consistency Audit references exactly one Replay Comparison.",
        "Replay Consistency Audit references exactly one "
        "Replay Reconstruction.",
        "Replay Consistency Audit may reference one Replay Failure.",
        "Replay Consistency Audit may reference one Replay Attestation.",
        "Replay Consistency Audit may reference one Replay Evidence.",
        "Replay Consistency Audit may reference one Replay Certification.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_audit_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Consistency Audit Ordering.",
        "Equivalent Replay Consistency Audits shall produce "
        "identical ordering.",
        "Implementation-defined ordering is prohibited.",
        "Ordering shall remain immutable.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_audit_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit shall preserve all mandatory "
        "Audit information.",
        "Replay Consistency Audit shall preserve all mandatory references.",
        "Replay Consistency Audit shall preserve all mandatory traceability.",
        "Replay Consistency Audit shall evaluate all mandatory "
        "Consistency Rules.",
        "Partial Replay Consistency Audit shall fail validation.",
        "Missing mandatory Audit information shall fail validation.",
        "Missing mandatory Consistency Findings shall fail validation.",
    ):
        assert requirement in content


def test_audit_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Archive.",
        "Replay Result.",
        "Replay Failure when present.",
        "Replay Attestation when present.",
        "Replay Evidence when present.",
        "Replay Certification when present.",
        "Replay Validation.",
        "Replay Comparison.",
        "Replay Reconstruction.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Audit Scope.",
        "Audit Status.",
        "Consistency Rules.",
        "Consistency Findings.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Consistency Audit shall never reinterpret preserved "
        "Replay artifacts.",
        "Replay Consistency Audit shall never normalize "
        "preserved information.",
        "Replay Consistency Audit shall never repair preserved information.",
        "Replay Consistency Audit shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Consistency Audit shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Replay Consistency Audit Identity.",
        "Replay Consistency Audit Version.",
        "Audit Identity.",
        "Audit Status.",
        "Audit Scope.",
        "Consistency Rules.",
        "Consistency Findings.",
        "Audit Integrity.",
        "Audit Traceability.",
        "Replay Archive Reference.",
        "Replay Result Reference.",
        "Replay Failure Reference.",
        "Replay Attestation Reference.",
        "Replay Evidence Reference.",
        "Replay Certification Reference.",
        "Replay Validation Reference.",
        "Replay Comparison Reference.",
        "Replay Reconstruction Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Consistency Audit Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Consistency Audit Ordering.",
        "Equivalent Replay Consistency Audits shall produce "
        "identical ordering.",
        "Implementation-defined ordering is prohibited.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in FAILURE_CONDITIONS:
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    assert "Replay Consistency Audit shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Consistency Audit shall never modify, reinterpret, "
        "normalize, repair, replace, merge, or suppress "
        "historical artifacts."
    ) in content

    assert (
        "Replay Consistency Audit shall preserve the original "
        "historical information exactly as recorded."
    ) in content


def test_replay_consistency_audit_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Consistency Audit shall remain immutable throughout "
        "its entire lifecycle."
    ) in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in SUCCESS_CRITERIA:
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for capability in RELEASE_CAPABILITIES:
        assert capability in content

    for exclusion in RELEASE_EXCLUSIONS:
        assert exclusion in content

    assert (
        "Future CKP-007 specifications shall preserve this "
        "Replay Consistency Audit Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.22" in content
    assert "Commerce Reasoning Replay Specification Freeze." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
