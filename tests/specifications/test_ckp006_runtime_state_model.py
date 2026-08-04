"""
Executable Specification

CKP-006.5
Commerce Runtime State Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_STATE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Runtime State Identity",
    "## Runtime State Version",
    "## Runtime State Lifecycle",
    "## Runtime State Status",
    "## Runtime State Scope",
    "## Runtime State Properties",
    "## Runtime State Snapshot",
    "## Runtime Working State",
    "## Runtime Terminal State",
    "## Runtime Stage Binding",
    "## Runtime Transition Binding",
    "## Runtime Artifact References",
    "## Runtime State Evolution",
    "## Runtime State Validation",
    "## Runtime State Integrity",
    "## Runtime State Traceability",
    "## Runtime State Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Runtime State Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Executing.",
    "Suspended.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

STATUS_VALUES = (
    "CREATED.",
    "INITIALIZED.",
    "EXECUTING.",
    "SUSPENDED.",
    "COMPLETED.",
    "FAILED.",
    "CANCELLED.",
)

STATE_PROPERTIES = (
    "Runtime State Identifier.",
    "Runtime State Version.",
    "Lifecycle.",
    "Status.",
    "Execution Context Reference.",
    "Execution Request Reference.",
    "Current Runtime Stage.",
    "Current Runtime Transition.",
    "Working State Reference.",
    "Snapshot Reference.",
    "Integrity Reference.",
    "Traceability Reference.",
)

SNAPSHOT_PROPERTIES = (
    "Current Stage.",
    "Current Transition.",
    "Resolved Facts.",
    "Evaluated Premises.",
    "Applicable Rules.",
    "Rule Applications.",
    "Variable Bindings.",
    "Derived Conclusions.",
    "Proof References.",
    "Evidence References.",
    "Explanation Reference when available.",
    "Validation Reference when available.",
    "Certification Reference when available.",
)

WORKING_STATE_CONTENTS = (
    "Resolved Facts.",
    "Evaluated Premises.",
    "Applicable Rules.",
    "Rejected Rules.",
    "Variable Bindings.",
    "Rule Applications.",
    "Derived Conclusions.",
    "Partial Proofs.",
    "Partial Evidence.",
    "Partial Explanations.",
)

ARTIFACT_REFERENCES = (
    "Fact References.",
    "Premise References.",
    "Rule References.",
    "Rule Application References.",
    "Variable Binding References.",
    "Derived Conclusion References.",
    "Proof References.",
    "Evidence References.",
    "Explanation References.",
    "Validation References.",
    "Certification References.",
)

FAILURE_CLASSIFICATIONS = (
    "STATE_IDENTITY_VIOLATION.",
    "STATE_VERSION_VIOLATION.",
    "STATE_LIFECYCLE_VIOLATION.",
    "STATE_STATUS_VIOLATION.",
    "STATE_STAGE_VIOLATION.",
    "STATE_TRANSITION_VIOLATION.",
    "STATE_SNAPSHOT_VIOLATION.",
    "STATE_WORKING_STATE_VIOLATION.",
    "STATE_TERMINAL_STATE_VIOLATION.",
    "STATE_REFERENCE_VIOLATION.",
    "STATE_VALIDATION_VIOLATION.",
    "STATE_INTEGRITY_VIOLATION.",
    "STATE_RELATIONSHIP_VIOLATION.",
    "STATE_SERIALIZATION_VIOLATION.",
    "STATE_ORDERING_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

STATE_INVARIANTS = (
    "Exactly one Identity.",
    "Exactly one Version.",
    "Exactly one Lifecycle.",
    "Exactly one Status.",
    "Exactly one Execution Context.",
    "Exactly one Execution Request.",
    "Exactly one Runtime Stage.",
    "Exactly one Runtime Transition.",
    "Exactly one Working State.",
    "Exactly one Snapshot.",
    "Exactly one Terminal State after completion.",
    "Deterministic Evolution.",
    "Deterministic Serialization.",
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
    assert "Title Commerce Runtime State Model" in content
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


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, replay-compatible, and "
        "integrity-preserving Runtime State maintained by "
        "the Commerce Reasoning Runtime.",
        "The Runtime State represents the complete execution "
        "state of exactly one Runtime Execution.",
        "The Runtime State specializes the Runtime Structure "
        "defined by CKP-006.2 and evolves under the Runtime "
        "Execution Context defined by CKP-006.4.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define execution algorithms.",
        "It does not define persistence.",
        "It does not define transport protocols.",
        "It does not define implementation classes.",
        "It does not define replay algorithms.",
        "It does not permit mutation after terminal completion.",
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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_runtime_state_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime State shall possess exactly one "
        "immutable Runtime State Identifier.",
        "CKP-RUNTIME-STATE-000001",
        "Runtime State Identity shall be globally unique.",
        "Runtime State Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Runtime "
        "State Identity shall fail validation.",
    ):
        assert requirement in content


def test_runtime_state_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime State shall declare exactly one Version.",
        "Version identifies the Runtime State schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_runtime_state_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Terminal lifecycle states shall remain immutable." in content
    assert "Lifecycle regression is prohibited." in content


def test_runtime_state_status_is_declared() -> None:
    content = normalized_text()

    for status in STATUS_VALUES:
        assert status in content

    assert (
        "Exactly one Runtime State Status shall exist at any time."
    ) in content


def test_runtime_state_scope_is_isolated() -> None:
    content = normalized_text()

    for requirement in (
        "One Runtime State shall belong to exactly one Runtime Execution.",
        "One Runtime State shall reference exactly one Execution Context.",
        "One Runtime State shall reference exactly one Execution Request.",
        "Runtime State sharing across Runtime Executions is prohibited.",
    ):
        assert requirement in content


def test_runtime_state_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in STATE_PROPERTIES:
        assert property_name in content


def test_runtime_state_snapshot_is_declared() -> None:
    content = normalized_text()

    assert "Every Runtime State shall expose one canonical Snapshot." in content

    for property_name in SNAPSHOT_PROPERTIES:
        assert property_name in content

    assert "Snapshot generation shall be deterministic." in content


def test_runtime_working_state_is_exactly_one_and_isolated() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Execution shall possess exactly one "
        "Runtime Working State."
    ) in content

    for artifact in WORKING_STATE_CONTENTS:
        assert artifact in content

    assert "Working State contents shall remain isolated." in content
    assert (
        "Working State contents shall never become canonical knowledge."
    ) in content


def test_runtime_terminal_state_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every terminal Runtime Execution shall produce exactly "
        "one immutable Runtime Terminal State."
    ) in content

    for property_name in (
        "Terminal Status.",
        "Final Runtime Stage.",
        "Final Runtime Transition.",
        "Final Conclusions.",
        "Final Proofs.",
        "Final Evidence.",
        "Final Validation Result.",
        "Final Certification Reference when applicable.",
    ):
        assert property_name in content

    assert "Runtime Terminal State shall never mutate." in content


def test_runtime_stage_binding_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime State shall reference exactly one Runtime Stage.",
        "Runtime Stage changes shall occur only through valid "
        "Runtime Transitions.",
        "Unknown Runtime Stages are prohibited.",
    ):
        assert requirement in content


def test_runtime_transition_binding_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime State transition shall reference exactly "
        "one Runtime Transition.",
        "Transition sequence numbers shall be strictly monotonic.",
        "Transition rollback is prohibited.",
        "Transition skipping is prohibited.",
    ):
        assert requirement in content


def test_runtime_artifact_references_are_declared() -> None:
    content = normalized_text()

    for reference in ARTIFACT_REFERENCES:
        assert reference in content

    assert "Every reference shall remain traceable." in content


def test_runtime_state_evolution_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Preserve Identity.",
        "Preserve Version.",
        "Preserve Traceability.",
        "Preserve Integrity.",
        "Respect Lifecycle.",
        "Respect Runtime Stage ordering.",
        "Respect Runtime Transition ordering.",
        "Terminate in exactly one terminal state.",
        "Evolution shall be deterministic.",
    ):
        assert requirement in content


def test_runtime_state_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Status.",
        "Execution Context.",
        "Execution Request.",
        "Runtime Stage.",
        "Runtime Transition.",
        "Snapshot.",
        "Working State.",
        "Terminal State.",
        "Artifact References.",
        "Integrity.",
        "Traceability.",
        "Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_runtime_state_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime State shall possess exactly one "
        "deterministic Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Status.",
        "Snapshot.",
        "Working State.",
        "Terminal State.",
        "Relationships.",
        "Serialization.",
        "Ordering.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Integrity." in content


def test_runtime_state_traceability_is_complete() -> None:
    content = normalized_text()

    for reference in (
        "Runtime State Identity.",
        "Runtime Execution Reference.",
        "Execution Context Reference.",
        "Execution Request Reference.",
        "Stage References.",
        "Transition References.",
        "Artifact References.",
        "Validation Reference.",
        "Replay Reference.",
        "Certification Reference when applicable.",
    ):
        assert reference in content

    assert "Traceability shall remain complete." in content


def test_runtime_state_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Belong to one Runtime Execution.",
        "Reference one Execution Context.",
        "Reference one Execution Request.",
        "Reference one Runtime Stage.",
        "Reference one Runtime Transition.",
        "Reference one Runtime Validation Result.",
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
        "Every Runtime State shall possess one canonical serialization."
    ) in content

    for property_name in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Status.",
        "Snapshot.",
        "Working State.",
        "Terminal State.",
        "Relationships.",
        "Integrity.",
    ):
        assert property_name in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for ordered_item in (
        "Runtime Stages.",
        "Runtime Transitions.",
        "Facts.",
        "Premises.",
        "Rules.",
        "Rule Applications.",
        "Variable Bindings.",
        "Derived Conclusions.",
        "Proofs.",
        "Evidence.",
        "Relationships.",
    ):
        assert ordered_item in content

    assert "Implementation-defined ordering is prohibited." in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Identity is invalid.",
        "Version is unsupported.",
        "Lifecycle is invalid.",
        "Status is invalid.",
        "Stage is invalid.",
        "Transition ordering is invalid.",
        "Snapshot cannot be produced.",
        "Working State is inconsistent.",
        "Terminal State is inconsistent.",
        "Artifact references cannot be resolved.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
        "Mutation occurs after terminal completion.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify Execution Context.",
        "Modify Execution Request.",
        "Modify Runtime Configuration.",
        "Modify Runtime Limits.",
        "Modify registered Facts.",
        "Modify registered Premises.",
        "Modify registered Rules.",
        "Modify Validation Results.",
        "Modify Certification Results.",
        "Modify Replay artifacts.",
        "Modify CKP-005 Baseline.",
        "Repair invalid state.",
        "Invent missing execution state.",
    ):
        assert prohibition in content


def test_runtime_state_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in STATE_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Lifecycle is valid.",
        "Status is valid.",
        "Execution Context is valid.",
        "Execution Request is valid.",
        "Stage is valid.",
        "Transition sequence is valid.",
        "Snapshot is complete.",
        "Working State is consistent.",
        "Terminal State is valid.",
        "Relationships resolve.",
        "Validation succeeds.",
        "Integrity is valid.",
        "Canonical serialization succeeds.",
        "Deterministic ordering succeeds.",
        "All invariants are preserved.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Runtime State Identity.",
        "Runtime State Version.",
        "Runtime State Lifecycle.",
        "Runtime State Status.",
        "Runtime State Scope.",
        "Runtime State Properties.",
        "Runtime State Snapshot.",
        "Runtime Working State.",
        "Runtime Terminal State.",
        "Runtime Stage Binding.",
        "Runtime Transition Binding.",
        "Runtime Artifact References.",
        "Runtime State Evolution.",
        "Runtime State Validation.",
        "Runtime State Integrity.",
        "Runtime State Traceability.",
        "Runtime State Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Boundary.",
        "Runtime State Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Execution algorithms.",
        "Persistence.",
        "Replay implementation.",
        "Event sourcing.",
        "Write-ahead logging.",
        "Concurrency.",
        "Distributed runtime coordination.",
        "Implementation classes.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-006 deliverables shall preserve "
        "this specification."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006.6" in content
    assert "Runtime Transition Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
