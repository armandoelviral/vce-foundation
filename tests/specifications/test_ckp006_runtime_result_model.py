"""
Executable Specification

CKP-006.9
Commerce Runtime Result Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_RESULT_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Runtime Result Identity",
    "## Runtime Result Version",
    "## Runtime Result Lifecycle",
    "## Runtime Result Status",
    "## Runtime Result Scope",
    "## Runtime Result Properties",
    "## Runtime Result Outcome",
    "## Runtime Result Inputs",
    "## Runtime Result Outputs",
    "## Runtime Result Success",
    "## Runtime Result Failure",
    "## Runtime Result Cancellation",
    "## Runtime Result Validation",
    "## Runtime Result Compatibility",
    "## Runtime Result Evidence",
    "## Runtime Result Integrity",
    "## Runtime Result Traceability",
    "## Runtime Result Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Runtime Result Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Validated.",
    "Finalized.",
    "Archived.",
)

RESULT_STATUSES = (
    "COMPLETED.",
    "FAILED.",
    "CANCELLED.",
)

RESULT_PROPERTIES = (
    "Runtime Result Identifier.",
    "Runtime Result Version.",
    "Runtime Result Status.",
    "Reasoning Status.",
    "Reasoning Outcome.",
    "Runtime Result Integrity.",
)

RESULT_INPUTS = (
    "Execution Request.",
    "Execution Context.",
    "Runtime Inputs.",
)

RESULT_OUTPUTS = (
    "Final Conclusions.",
    "Proof References.",
    "Reasoning Evidence.",
    "Runtime Evidence.",
    "Explanation.",
    "Validation Result.",
    "Certification Reference when applicable.",
    "Failure Reference when applicable.",
    "Replay Descriptor.",
)

FAILURE_CLASSIFICATIONS = (
    "RUNTIME_RESULT_IDENTITY_VIOLATION.",
    "RUNTIME_RESULT_VERSION_VIOLATION.",
    "RUNTIME_RESULT_STATUS_VIOLATION.",
    "RUNTIME_RESULT_OUTCOME_VIOLATION.",
    "RUNTIME_RESULT_INPUT_VIOLATION.",
    "RUNTIME_RESULT_OUTPUT_VIOLATION.",
    "RUNTIME_RESULT_COMPATIBILITY_VIOLATION.",
    "RUNTIME_RESULT_EVIDENCE_VIOLATION.",
    "RUNTIME_RESULT_INTEGRITY_VIOLATION.",
    "RUNTIME_RESULT_TRACEABILITY_VIOLATION.",
    "RUNTIME_RESULT_RELATIONSHIP_VIOLATION.",
    "RUNTIME_RESULT_SERIALIZATION_VIOLATION.",
    "RUNTIME_RESULT_ORDERING_VIOLATION.",
    "RUNTIME_RESULT_VALIDATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

RESULT_INVARIANTS = (
    "Exactly one Runtime Result Identity.",
    "Exactly one Runtime Result Version.",
    "Exactly one Runtime Execution.",
    "Exactly one Runtime Result Status.",
    "Exactly one Runtime Result Outcome.",
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

    assert "# CKP-006" in content
    assert "Title Commerce Runtime Result Model" in content
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


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, replay-compatible, and "
        "integrity-preserving Runtime Result governing the "
        "terminal outcome of exactly one Runtime Execution.",
        "A Runtime Result represents exactly one final Outcome "
        "of exactly one Runtime Execution.",
        "This specification defines Runtime Result identity, "
        "lifecycle, status, scope, properties, outcomes, "
        "validation, compatibility, evidence, integrity, "
        "traceability, relationships, serialization, failure "
        "semantics, and structural invariants.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define execution algorithms.",
        "It does not define Runtime Result implementation.",
        "It does not define persistence.",
        "It does not define WAL.",
        "It does not define event sourcing.",
        "It does not define transport.",
        "It does not define schedulers.",
        "It does not define concurrency.",
        "It does not define replay engines.",
        "It does not define hashing algorithms.",
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
        "CKP-006.1 Commerce Reasoning Runtime Charter.",
        "CKP-006.2 Runtime Structure Model.",
        "CKP-006.3 Runtime Execution Request Model.",
        "CKP-006.4 Runtime Execution Context Model.",
        "CKP-006.5 Runtime State Model.",
        "CKP-006.6 Runtime Transition Model.",
        "CKP-006.7 Runtime Stage Model.",
        "CKP-006.8 Runtime Artifact Registry Model.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_result_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Result shall possess exactly one "
        "immutable Runtime Result Identifier.",
        "CKP-RUNTIME-RESULT-000001",
        "Runtime Result Identity shall be globally unique.",
        "Runtime Result Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Runtime "
        "Result Identity shall fail validation.",
    ):
        assert requirement in content


def test_result_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Result shall declare exactly one Version.",
        "Version identifies the Runtime Result schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_result_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Terminal lifecycle states shall remain immutable." in content
    assert "Lifecycle regression is prohibited." in content


def test_result_status_is_exactly_one_and_closed() -> None:
    content = normalized_text()

    assert (
        "Exactly one Runtime Result Status shall be declared."
    ) in content

    for status in RESULT_STATUSES:
        assert status in content

    assert (
        "Undefined Runtime Result Status values are prohibited."
    ) in content


def test_result_scope_is_exactly_one_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Runtime Result shall belong to exactly one "
        "Runtime Execution.",
        "Runtime Result sharing across Runtime Executions "
        "is prohibited.",
    ):
        assert requirement in content


def test_result_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in RESULT_PROPERTIES:
        assert property_name in content


def test_result_outcome_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Result shall declare exactly one "
        "terminal Outcome.",
        "The terminal Outcome shall be immutable.",
        "Outcome changes after finalization are prohibited.",
    ):
        assert requirement in content


def test_result_inputs_are_declared_and_immutable() -> None:
    content = normalized_text()

    for result_input in RESULT_INPUTS:
        assert result_input in content

    assert "Referenced Inputs shall remain immutable." in content


def test_result_outputs_are_declared_and_immutable() -> None:
    content = normalized_text()

    for result_output in RESULT_OUTPUTS:
        assert result_output in content

    assert (
        "Outputs shall remain immutable after finalization."
    ) in content


def test_success_result_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Result Status equals COMPLETED.",
        "Successful Validation.",
        "Integrity preservation.",
        "Deterministic completion.",
        "Complete traceability.",
    ):
        assert requirement in content


def test_failed_result_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Result Status equals FAILED.",
        "Failure Reference.",
        "Validation outcome.",
        "Integrity preservation.",
        "Traceability preservation.",
    ):
        assert requirement in content


def test_cancelled_result_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Result Status equals CANCELLED.",
        "Explicit cancellation.",
        "Deterministic termination.",
        "Traceability preservation.",
    ):
        assert requirement in content


def test_result_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Status.",
        "Scope.",
        "Inputs.",
        "Outputs.",
        "Outcome.",
        "Compatibility.",
        "Evidence.",
        "Integrity.",
        "Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_result_compatibility_is_declared() -> None:
    content = normalized_text()

    for compatible_artifact in (
        "Runtime State.",
        "Runtime Stage.",
        "Runtime Transition.",
        "Artifact Registry.",
    ):
        assert compatible_artifact in content

    assert "Validation incompatibility shall fail." in content


def test_result_evidence_is_declared_and_immutable() -> None:
    content = normalized_text()

    for evidence_reference in (
        "Reasoning Evidence.",
        "Runtime Evidence.",
        "Validation Result.",
        "Certification Reference when applicable.",
        "Failure Reference when applicable.",
    ):
        assert evidence_reference in content

    assert "Evidence shall remain immutable." in content


def test_result_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Result shall possess exactly one "
        "deterministic Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Status.",
        "Outcome.",
        "Outputs.",
        "Relationships.",
        "Serialization.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Integrity." in content


def test_result_traceability_is_complete() -> None:
    content = normalized_text()

    for reference in (
        "Runtime Result Identity.",
        "Runtime Execution Reference.",
        "Runtime State Reference.",
        "Runtime Stage Reference.",
        "Runtime Transition Reference.",
        "Validation Reference.",
        "Replay Reference.",
        "Certification Reference when applicable.",
    ):
        assert reference in content

    assert "Traceability shall remain complete." in content


def test_result_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Belong to one Runtime Execution.",
        "Reference one Runtime State.",
        "Reference one Runtime Stage.",
        "Reference one Runtime Transition.",
        "Reference one Artifact Registry.",
        "Reference one Validation Result.",
        "Reference one Replay Descriptor.",
    ):
        assert relationship in content

    assert (
        "Every relationship shall be explicit, deterministic, "
        "traceable, and integrity-bound."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Result shall possess one canonical serialization."
    ) in content

    for property_name in (
        "Identity.",
        "Version.",
        "Status.",
        "Outcome.",
        "Outputs.",
        "Relationships.",
        "Integrity.",
    ):
        assert property_name in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Results shall possess one canonical ordering.",
        "Ordering shall be deterministic.",
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
        "Runtime Result Identity is invalid.",
        "Runtime Result Version is unsupported.",
        "Runtime Result Status is invalid.",
        "Outcome is undefined.",
        "Required Inputs are missing.",
        "Required Outputs are missing.",
        "Compatibility verification fails.",
        "Evidence verification fails.",
        "Integrity verification fails.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
        "Mutation occurs after finalization.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Runtime State.",
        "Runtime Stage.",
        "Runtime Transition.",
        "Artifact Registry.",
        "Execution Context.",
        "Execution Request.",
        "Registered Facts.",
        "Registered Premises.",
        "Registered Rules.",
        "CKP-005 Baseline.",
    ):
        assert target in content

    assert "The Runtime Result shall not modify:" in content


def test_result_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in RESULT_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Status is valid.",
        "Outcome is valid.",
        "Inputs are complete.",
        "Outputs are complete.",
        "Compatibility succeeds.",
        "Validation succeeds.",
        "Integrity is valid.",
        "Relationships resolve.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Runtime Result Identity.",
        "Runtime Result Version.",
        "Runtime Result Lifecycle.",
        "Runtime Result Status.",
        "Runtime Result Scope.",
        "Runtime Result Properties.",
        "Runtime Result Outcome.",
        "Runtime Result Inputs.",
        "Runtime Result Outputs.",
        "Runtime Result Success.",
        "Runtime Result Failure.",
        "Runtime Result Cancellation.",
        "Runtime Result Validation.",
        "Runtime Result Compatibility.",
        "Runtime Result Evidence.",
        "Runtime Result Integrity.",
        "Runtime Result Traceability.",
        "Runtime Result Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Boundary.",
        "Runtime Result Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Execution algorithms.",
        "Runtime Result implementation.",
        "Persistence.",
        "Write-ahead logging.",
        "Event sourcing.",
        "Transport.",
        "Schedulers.",
        "Concurrency.",
        "Replay implementation.",
        "Hashing algorithms.",
        "Implementation classes.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-006 deliverables shall preserve "
        "this specification."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006.10" in content
    assert "Runtime Specification Freeze." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
