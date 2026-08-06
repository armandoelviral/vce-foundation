"""
Executable Specification

CKP-007.20
Commerce Replay Archive Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_ARCHIVE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Archive Identity",
    "## Replay Archive Version",
    "## Replay Archive Lifecycle",
    "## Replay Archive Scope",
    "## Replay Archive Inputs",
    "## Replay Archive Preconditions",
    "## Replay Result Reference",
    "## Replay Failure Reference",
    "## Replay Attestation Reference",
    "## Replay Evidence Reference",
    "## Replay Certification Reference",
    "## Archive Identity",
    "## Archive Status",
    "## Archive Composition",
    "## Archive Retention",
    "## Archive Closure",
    "## Archive Integrity",
    "## Archive Traceability",
    "## Archive Relationships",
    "## Archive Ordering",
    "## Archive Completeness",
    "## Archive Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Archive Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Archived.",
    "Preserved.",
)

ARCHIVE_STATUSES = (
    "OPEN.",
    "CLOSED.",
    "PRESERVED.",
)

REQUIRED_INPUTS = (
    "Replay Archive Identifier.",
    "Replay Archive Version.",
    "Replay Result Reference.",
    "Replay Failure Reference.",
    "Replay Attestation Reference.",
    "Replay Evidence Reference.",
    "Replay Certification Reference.",
    "Archive Identifier.",
    "Archive Status.",
    "Archive Composition.",
    "Archive Retention.",
    "Archive Closure.",
    "Archive Integrity Reference.",
    "Archive Traceability Reference.",
    "Replay Archive Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Result.",
    "Resolved Replay Integrity.",
    "Resolved Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Archive shall preserve exactly one Replay.",
    "Replay Archive shall require exactly one Replay Result.",
    "Replay Archive shall preserve Replay Failure when present.",
    "Replay Archive shall preserve Replay Attestation when present.",
    "Replay Archive shall preserve Replay Evidence when present.",
    "Replay Archive shall preserve Replay Certification when present.",
    "Replay Archive shall preserve Replay Integrity.",
    "Replay Archive shall preserve Replay Traceability.",
    "Replay Archive shall be deterministic.",
    "Replay Archive shall remain immutable.",
    "Replay Archive shall fail closed.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_ARCHIVE_IDENTITY_VIOLATION.",
    "REPLAY_ARCHIVE_VERSION_VIOLATION.",
    "REPLAY_ARCHIVE_LIFECYCLE_VIOLATION.",
    "REPLAY_ARCHIVE_SCOPE_VIOLATION.",
    "REPLAY_ARCHIVE_INPUT_VIOLATION.",
    "REPLAY_ARCHIVE_PRECONDITION_VIOLATION.",
    "REPLAY_ARCHIVE_REFERENCE_VIOLATION.",
    "ARCHIVE_STATUS_VIOLATION.",
    "ARCHIVE_COMPOSITION_VIOLATION.",
    "ARCHIVE_RETENTION_VIOLATION.",
    "ARCHIVE_CLOSURE_VIOLATION.",
    "ARCHIVE_INTEGRITY_VIOLATION.",
    "ARCHIVE_TRACEABILITY_VIOLATION.",
    "ARCHIVE_RELATIONSHIP_VIOLATION.",
    "ARCHIVE_ORDERING_VIOLATION.",
    "ARCHIVE_COMPLETENESS_VIOLATION.",
    "ARCHIVE_CONSISTENCY_VIOLATION.",
    "REPLAY_ARCHIVE_SERIALIZATION_VIOLATION.",
    "REPLAY_ARCHIVE_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Archive Identity is invalid.",
    "Replay Archive Version is unsupported.",
    "Mandatory inputs are missing.",
    "Replay Result cannot be resolved.",
    "Archive Status is invalid.",
    "Archive Composition is invalid.",
    "Archive Retention is invalid.",
    "Archive Closure is invalid.",
    "Archive Integrity verification fails.",
    "Archive Traceability verification fails.",
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
    "Historical Replay Certification.",
    "Historical Replay Evidence.",
    "Historical Replay Attestation.",
    "Historical Replay Failure.",
    "Historical Replay Archive.",
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Archive Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Result.",
    "Exactly one Archive Composition.",
    "Exactly one Replay Archive Integrity Reference.",
    "Identity Preservation.",
    "Result Preservation.",
    "Archive Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Archive.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Result resolves successfully.",
    "Archive Status is valid.",
    "Archive Composition is complete.",
    "Archive Retention is valid.",
    "Archive Closure is valid.",
    "Archive Integrity is verified.",
    "Archive Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Archive Identity.",
    "Replay Archive Version.",
    "Replay Archive Lifecycle.",
    "Replay Archive Scope.",
    "Replay Archive Inputs.",
    "Replay Archive Preconditions.",
    "Replay Result Reference.",
    "Replay Failure Reference.",
    "Replay Certification Reference.",
    "Replay Evidence Reference.",
    "Replay Attestation Reference.",
    "Archive Identity.",
    "Archive Status.",
    "Archive Composition.",
    "Archive Retention.",
    "Archive Closure.",
    "Archive Integrity.",
    "Archive Traceability.",
    "Archive Relationships.",
    "Archive Ordering.",
    "Archive Completeness.",
    "Archive Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Archive Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Archive engine.",
    "Storage engine.",
    "Filesystem layout.",
    "Object storage.",
    "Retention scheduler.",
    "Deletion engine.",
    "Compression algorithms.",
    "Encryption algorithms.",
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
    assert "Title Commerce Replay Archive Model" in content
    assert "Abbreviation CRAM" in content
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


def test_archive_statuses_are_exact() -> None:
    content = normalized_text()

    assert (
        "Every Replay Archive shall declare exactly one Archive Status."
        in content
    )

    for status in ARCHIVE_STATUSES:
        assert status in content

    assert "Unsupported Archive Status shall fail validation." in content
    assert (
        "Replay Archive Lifecycle and Archive Status shall remain "
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


def test_replay_result_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall reference exactly one immutable Replay Result.",
        "Replay Result Reference shall remain resolvable.",
        "Replay Result Reference shall remain immutable.",
        "Replay Result Reference shall preserve traceability.",
        "Missing Replay Result Reference shall fail validation.",
    ):
        assert requirement in content


def test_conditional_references_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall reference exactly one Replay Failure "
        "when present.",
        "Replay Archive shall reference exactly one Replay Attestation "
        "when present.",
        "Replay Archive shall reference exactly one Replay Evidence "
        "when present.",
        "Replay Archive shall reference exactly one Replay Certification "
        "when present.",
    ):
        assert requirement in content


def test_archive_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Archive shall possess exactly one immutable Archive Identifier.",
        "Archive Identity shall be globally unique.",
        "Archive Identity shall never be reused.",
        "Missing Archive Identifier shall fail validation.",
        "Malformed Archive Identifier shall fail validation.",
        "Duplicated Archive Identifier shall fail validation.",
    ):
        assert requirement in content


def test_archive_composition_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall declare exactly one Archive Composition.",
        "Archive Composition shall identify the complete preserved "
        "Replay artifact set.",
        "Archive Composition shall remain immutable.",
        "Archive Composition shall remain fully traceable.",
        "Missing Archive Composition shall fail validation.",
        "Incomplete Archive Composition shall fail validation.",
    ):
        assert requirement in content


def test_archive_retention_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall declare exactly one Archive Retention.",
        "Archive Retention shall define the normative preservation scope.",
        "Archive Retention shall remain immutable.",
        "Archive Retention shall remain fully traceable.",
        "Missing Archive Retention shall fail validation.",
    ):
        assert requirement in content


def test_archive_closure_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall declare exactly one Archive Closure.",
        "Archive Closure shall identify the terminal closure state "
        "of the Replay Archive.",
        "Archive Closure shall remain immutable.",
        "Archive Closure shall remain completely traceable.",
        "Missing Archive Closure shall fail validation.",
    ):
        assert requirement in content


def test_archive_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Archive shall possess exactly one deterministic "
        "Archive Integrity Reference."
    ) in content

    for binding in (
        "Replay Archive Identity.",
        "Replay Archive Version.",
        "Archive Identity.",
        "Archive Status.",
        "Archive Composition.",
        "Archive Retention.",
        "Archive Closure.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Archive Integrity." in content
    assert "Archive Integrity shall remain immutable." in content


def test_archive_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Result.",
        "Replay Failure.",
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Attestation.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Archive Composition.",
    ):
        assert target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_archive_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Archive belongs to exactly one Replay.",
        "Replay Archive references exactly one Replay Result.",
        "Replay Archive may reference one Replay Failure.",
        "Replay Archive may reference one Replay Certification.",
        "Replay Archive may reference one Replay Evidence.",
        "Replay Archive may reference one Replay Attestation.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_archive_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Archive Ordering.",
        "Equivalent Replay Archives shall produce identical ordering.",
        "Implementation-defined ordering is prohibited.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_archive_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive shall preserve all mandatory Archive information.",
        "Replay Archive shall preserve all mandatory references.",
        "Replay Archive shall preserve all mandatory traceability.",
        "Partial Replay Archive shall fail validation.",
        "Missing mandatory Archive information shall fail validation.",
    ):
        assert requirement in content


def test_archive_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Result.",
        "Replay Failure.",
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Attestation.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Archive Composition.",
        "Archive Status.",
        "Archive Retention.",
        "Archive Closure.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Archive shall never reinterpret preserved Replay artifacts.",
        "Replay Archive shall never normalize preserved information.",
        "Replay Archive shall never repair preserved information.",
        "Replay Archive shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Archive shall possess exactly one canonical serialization."
        in content
    )

    for preserved_property in (
        "Replay Archive Identity.",
        "Replay Archive Version.",
        "Archive Identity.",
        "Archive Status.",
        "Archive Composition.",
        "Archive Retention.",
        "Archive Closure.",
        "Archive Integrity.",
        "Archive Traceability.",
        "Replay Result Reference.",
        "Replay Failure Reference.",
        "Replay Certification Reference.",
        "Replay Evidence Reference.",
        "Replay Attestation Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Archive Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Archive Ordering.",
        "Equivalent Replay Archives shall produce identical ordering.",
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

    assert "Replay Archive shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Archive shall never modify, reinterpret, normalize, repair, "
        "replace, merge, or suppress historical artifacts."
    ) in content

    assert (
        "Replay Archive shall preserve the original historical information "
        "exactly as recorded."
    ) in content


def test_replay_archive_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Archive shall remain immutable throughout its entire lifecycle."
        in content
    )


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
        "Replay Archive Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.21" in content
    assert "Replay Consistency Audit Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
