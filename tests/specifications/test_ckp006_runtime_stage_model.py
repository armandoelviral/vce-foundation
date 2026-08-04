"""
Executable Specification

CKP-006.7
Commerce Runtime Stage Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_STAGE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Runtime Stage Identity",
    "## Runtime Stage Version",
    "## Runtime Stage Lifecycle",
    "## Runtime Stage Scope",
    "## Canonical Runtime Stages",
    "## Stage Classification",
    "## Stage Preconditions",
    "## Stage Inputs",
    "## Stage Outputs",
    "## Stage Entry",
    "## Stage Execution Boundary",
    "## Stage Completion",
    "## Stage Failure",
    "## Stage Cancellation",
    "## Stage Transition Compatibility",
    "## Stage Lifecycle Compatibility",
    "## Stage Ordering",
    "## Stage Determinism",
    "## Stage Validation",
    "## Stage Integrity",
    "## Stage Traceability",
    "## Stage Relationships",
    "## Canonical Serialization",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Runtime Stage Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Defined.",
    "Available.",
    "Entered.",
    "Executing.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

CANONICAL_STAGES = (
    "Admission.",
    "Validation.",
    "Preparation.",
    "Inference.",
    "Proof Construction.",
    "Evidence Collection.",
    "Explanation Generation.",
    "Certification.",
    "Completion.",
    "Failure.",
    "Cancellation.",
)

STAGE_CLASSIFICATIONS = (
    "Execution Stage.",
    "Verification Stage.",
    "Evidence Stage.",
    "Terminal Stage.",
)

FAILURE_CLASSIFICATIONS = (
    "STAGE_IDENTITY_VIOLATION.",
    "STAGE_VERSION_VIOLATION.",
    "STAGE_PRECONDITION_VIOLATION.",
    "STAGE_INPUT_VIOLATION.",
    "STAGE_OUTPUT_VIOLATION.",
    "STAGE_TRANSITION_VIOLATION.",
    "STAGE_LIFECYCLE_VIOLATION.",
    "STAGE_ORDERING_VIOLATION.",
    "STAGE_DETERMINISM_VIOLATION.",
    "STAGE_VALIDATION_VIOLATION.",
    "STAGE_INTEGRITY_VIOLATION.",
    "STAGE_RELATIONSHIP_VIOLATION.",
    "STAGE_SERIALIZATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

STAGE_INVARIANTS = (
    "Exactly one Identity.",
    "Exactly one Version.",
    "Exactly one Classification.",
    "Exactly one Runtime Execution.",
    "Exactly one Runtime State.",
    "Exactly one Runtime Transition.",
    "Canonical Ordering.",
    "Deterministic Execution.",
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
    assert "Title Commerce Runtime Stage Model" in content
    assert "Abbreviation CRSGM" in content
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
        "integrity-preserving Runtime Stage model governing "
        "the execution progress of the Commerce Reasoning Runtime.",
        "A Runtime Stage represents exactly one canonical "
        "execution stage of exactly one Runtime Execution.",
        "This specification defines Runtime Stage identity, "
        "lifecycle, scope, canonical stages, classification, "
        "preconditions, inputs, outputs, execution boundaries, "
        "completion, failure, cancellation, compatibility, "
        "ordering, determinism, validation, integrity, "
        "traceability, relationships, serialization, failure "
        "semantics, and structural invariants.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define execution algorithms.",
        "It does not define stage implementations.",
        "It does not define schedulers.",
        "It does not define concurrency.",
        "It does not define persistence.",
        "It does not define WAL.",
        "It does not define event sourcing.",
        "It does not define replay engines.",
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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_stage_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall possess exactly one "
        "immutable Runtime Stage Identifier.",
        "CKP-RUNTIME-STAGE-000001",
        "Runtime Stage Identity shall be globally unique.",
        "Runtime Stage Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Runtime "
        "Stage Identity shall fail validation.",
    ):
        assert requirement in content


def test_stage_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare exactly one Version.",
        "Version identifies the Runtime Stage schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_stage_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Terminal lifecycle states shall remain immutable." in content
    assert "Lifecycle regression is prohibited." in content


def test_stage_scope_is_exactly_one_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Runtime Stage shall belong to exactly one "
        "Runtime Execution.",
        "One Runtime Stage shall exist exactly once within "
        "one Runtime State progression.",
        "Runtime Stage sharing across Runtime Executions "
        "is prohibited.",
    ):
        assert requirement in content


def test_canonical_runtime_stages_are_declared() -> None:
    content = normalized_text()

    for stage in CANONICAL_STAGES:
        assert stage in content

    assert (
        "No additional Runtime Stages shall exist in Version 1.0."
    ) in content


def test_stage_classification_is_exactly_one() -> None:
    content = normalized_text()

    for classification in STAGE_CLASSIFICATIONS:
        assert classification in content

    assert (
        "Exactly one classification shall apply to each "
        "Runtime Stage."
    ) in content


def test_stage_preconditions_are_mandatory() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare exactly one "
        "set of mandatory Preconditions.",
        "Preconditions shall be validated before stage entry.",
        "Unmet Preconditions shall prevent stage entry.",
    ):
        assert requirement in content


def test_stage_inputs_are_declared_and_closed() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare its required Inputs.",
        "Undeclared Inputs shall not participate in the "
        "Runtime Stage.",
        "Input completeness shall be validated before execution.",
    ):
        assert requirement in content


def test_stage_outputs_are_declared_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare its canonical Outputs.",
        "Outputs shall become immutable upon successful completion.",
        "Partial Outputs are prohibited.",
    ):
        assert requirement in content


def test_stage_entry_is_gated_and_exactly_once() -> None:
    content = normalized_text()

    for requirement in (
        "Successful Preconditions.",
        "Successful Validation.",
        "Compatible Runtime Transition.",
        "Compatible Lifecycle State.",
        "Stage entry shall occur exactly once.",
    ):
        assert requirement in content


def test_stage_execution_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall define one execution boundary.",
        "Execution outside the declared boundary is prohibited.",
    ):
        assert requirement in content


def test_stage_completion_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Completed execution.",
        "Successful validation.",
        "Integrity preservation.",
        "Traceability preservation.",
        "Completed Runtime Transition.",
    ):
        assert requirement in content


def test_stage_failure_is_terminal_and_traceable() -> None:
    content = normalized_text()

    for requirement in (
        "Stage Failure shall terminate the current Runtime Stage.",
        "Failure shall be deterministic.",
        "Failure shall be traceable.",
    ):
        assert requirement in content


def test_stage_cancellation_is_explicit_and_traceable() -> None:
    content = normalized_text()

    for requirement in (
        "Stage Cancellation shall terminate the current "
        "Runtime Stage without successful completion.",
        "Cancellation shall be explicit.",
        "Cancellation shall be traceable.",
    ):
        assert requirement in content


def test_stage_transition_compatibility_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare compatible incoming "
        "and outgoing Runtime Transitions.",
        "Incompatible Runtime Transitions shall fail validation.",
    ):
        assert requirement in content


def test_stage_lifecycle_compatibility_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Stage shall declare compatible "
        "Lifecycle states.",
        "Lifecycle incompatibility shall fail validation.",
    ):
        assert requirement in content


def test_stage_ordering_is_canonical_and_strict() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Stages shall possess one canonical ordering.",
        "Stage reordering is prohibited.",
        "Stage skipping is prohibited.",
        "Stage rollback is prohibited.",
    ):
        assert requirement in content


def test_stage_determinism_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Equivalent Runtime Inputs shall always produce "
        "the same Runtime Stage progression.",
        "Implementation-defined Runtime Stage behavior "
        "is prohibited.",
        "Non-deterministic Runtime Stage execution is prohibited.",
    ):
        assert requirement in content


def test_stage_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Scope.",
        "Classification.",
        "Preconditions.",
        "Inputs.",
        "Outputs.",
        "Transition Compatibility.",
        "Lifecycle Compatibility.",
        "Ordering.",
        "Determinism.",
        "Integrity.",
        "Relationships.",
        "Canonical Serialization.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_stage_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Stage shall possess exactly one "
        "deterministic Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Classification.",
        "Inputs.",
        "Outputs.",
        "Ordering.",
        "Relationships.",
        "Serialization.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Integrity." in content


def test_stage_traceability_is_complete() -> None:
    content = normalized_text()

    for reference in (
        "Runtime Stage Identity.",
        "Runtime State Reference.",
        "Runtime Transition Reference.",
        "Execution Context Reference.",
        "Execution Request Reference.",
        "Validation Reference.",
        "Replay Reference.",
        "Certification Reference when applicable.",
    ):
        assert reference in content

    assert "Traceability shall remain complete." in content


def test_stage_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Belong to one Runtime Execution.",
        "Reference one Runtime State.",
        "Reference one Runtime Transition.",
        "Reference one Validation Result.",
        "Participate in one Replay Descriptor.",
    ):
        assert relationship in content

    assert (
        "Every relationship shall be explicit, deterministic, "
        "traceable, and integrity-bound."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Stage shall possess one canonical serialization."
    ) in content

    for property_name in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Classification.",
        "Inputs.",
        "Outputs.",
        "Ordering.",
        "Relationships.",
        "Integrity.",
    ):
        assert property_name in content

    assert "Canonical serialization shall be deterministic." in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Identity is invalid.",
        "Version is unsupported.",
        "Preconditions fail.",
        "Required Inputs are missing.",
        "Required Outputs are invalid.",
        "Transition compatibility fails.",
        "Lifecycle compatibility fails.",
        "Ordering is invalid.",
        "Determinism cannot be verified.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Mutation occurs after completion.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify Runtime Configuration.",
        "Modify Runtime Limits.",
        "Modify Runtime Execution Context.",
        "Modify Runtime Execution Request.",
        "Modify Runtime State.",
        "Modify registered Facts.",
        "Modify registered Premises.",
        "Modify registered Rules.",
        "Modify CKP-005 Baseline.",
        "Repair invalid Runtime Stages.",
        "Invent missing Runtime Stage state.",
    ):
        assert prohibition in content


def test_stage_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in STAGE_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Preconditions succeed.",
        "Inputs are complete.",
        "Outputs are complete.",
        "Transition compatibility succeeds.",
        "Lifecycle compatibility succeeds.",
        "Ordering is valid.",
        "Determinism is preserved.",
        "Validation succeeds.",
        "Integrity is valid.",
        "Relationships resolve.",
        "Canonical serialization succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Runtime Stage Identity.",
        "Runtime Stage Version.",
        "Runtime Stage Lifecycle.",
        "Runtime Stage Scope.",
        "Canonical Runtime Stages.",
        "Stage Classification.",
        "Stage Preconditions.",
        "Stage Inputs.",
        "Stage Outputs.",
        "Stage Entry.",
        "Stage Execution Boundary.",
        "Stage Completion.",
        "Stage Failure.",
        "Stage Cancellation.",
        "Stage Transition Compatibility.",
        "Stage Lifecycle Compatibility.",
        "Stage Ordering.",
        "Stage Determinism.",
        "Stage Validation.",
        "Stage Integrity.",
        "Stage Traceability.",
        "Stage Relationships.",
        "Canonical Serialization.",
        "Failure Behavior.",
        "Read-Only Boundary.",
        "Runtime Stage Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Execution algorithms.",
        "Stage implementations.",
        "Schedulers.",
        "Concurrency.",
        "Persistence.",
        "Write-ahead logging.",
        "Event sourcing.",
        "Replay implementation.",
        "Implementation classes.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-006 deliverables shall preserve "
        "this specification."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006.8" in content
    assert "Runtime Artifact Registry Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
