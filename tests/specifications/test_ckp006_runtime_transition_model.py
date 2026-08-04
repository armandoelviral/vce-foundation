"""
Executable Specification

CKP-006.6
Commerce Runtime Transition Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_TRANSITION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Runtime Transition Identity",
    "## Runtime Transition Version",
    "## Runtime Transition Lifecycle",
    "## Runtime Transition Scope",
    "## Runtime Transition Trigger",
    "## Runtime Transition Preconditions",
    "## Runtime Transition Source State",
    "## Runtime Transition Target State",
    "## Runtime Transition Validation",
    "## Runtime Transition Ordering",
    "## Runtime Transition Atomicity",
    "## Runtime Transition Determinism",
    "## Runtime Transition Integrity",
    "## Runtime Transition Traceability",
    "## Runtime Transition Relationships",
    "## Canonical Serialization",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Runtime Transition Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Validated.",
    "Authorized.",
    "Applied.",
    "Completed.",
    "Failed.",
    "Cancelled.",
)

TRIGGER_CLASSES = (
    "Validation Success.",
    "Rule Evaluation.",
    "Rule Application.",
    "Inference Completion.",
    "Proof Completion.",
    "Evidence Completion.",
    "Explanation Completion.",
    "Execution Failure.",
    "Execution Cancellation.",
)

PRECONDITIONS = (
    "Identity validity.",
    "Version compatibility.",
    "Trigger validity.",
    "Source State validity.",
    "Target State validity.",
    "Ordering validity.",
    "Integrity validity.",
)

FAILURE_CLASSIFICATIONS = (
    "TRANSITION_IDENTITY_VIOLATION.",
    "TRANSITION_VERSION_VIOLATION.",
    "TRANSITION_TRIGGER_VIOLATION.",
    "TRANSITION_PRECONDITION_VIOLATION.",
    "TRANSITION_SOURCE_STATE_VIOLATION.",
    "TRANSITION_TARGET_STATE_VIOLATION.",
    "TRANSITION_ORDERING_VIOLATION.",
    "TRANSITION_ATOMICITY_VIOLATION.",
    "TRANSITION_DETERMINISM_VIOLATION.",
    "TRANSITION_VALIDATION_VIOLATION.",
    "TRANSITION_INTEGRITY_VIOLATION.",
    "TRANSITION_RELATIONSHIP_VIOLATION.",
    "TRANSITION_SERIALIZATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

TRANSITION_INVARIANTS = (
    "Exactly one Identity.",
    "Exactly one Version.",
    "Exactly one Trigger.",
    "Exactly one Source State.",
    "Exactly one Target State.",
    "Exactly one Transition Sequence Number.",
    "Strict Monotonic Ordering.",
    "Atomic Execution.",
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
    assert "Title Commerce Runtime Transition Model" in content
    assert "Abbreviation CRTM" in content
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
        "integrity-preserving Runtime Transition governing "
        "state evolution within the Commerce Reasoning Runtime.",
        "A Runtime Transition represents exactly one authorized "
        "state change of exactly one Runtime State.",
        "This specification defines Runtime Transition identity, "
        "lifecycle, scope, triggers, preconditions, validation, "
        "ordering, atomicity, determinism, integrity, traceability, "
        "relationships, serialization, failure semantics, and "
        "structural invariants.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define execution algorithms.",
        "It does not define state-machine implementations.",
        "It does not define persistence.",
        "It does not define WAL.",
        "It does not define event sourcing.",
        "It does not define schedulers.",
        "It does not define concurrency.",
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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_transition_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall possess exactly one "
        "immutable Runtime Transition Identifier.",
        "CKP-RUNTIME-TRANSITION-000001",
        "Runtime Transition Identity shall be globally unique.",
        "Runtime Transition Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Runtime "
        "Transition Identity shall fail validation.",
    ):
        assert requirement in content


def test_transition_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall declare exactly one Version.",
        "Version identifies the Runtime Transition schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_transition_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Terminal lifecycle states shall remain immutable." in content
    assert "Lifecycle regression is prohibited." in content


def test_transition_scope_is_exactly_one_state() -> None:
    content = normalized_text()

    for requirement in (
        "One Runtime Transition shall belong to exactly one "
        "Runtime State.",
        "One Runtime Transition shall reference exactly one "
        "Runtime Stage transition.",
        "Runtime Transition sharing across Runtime States is prohibited.",
    ):
        assert requirement in content


def test_transition_trigger_is_exactly_one() -> None:
    content = normalized_text()

    assert "Every Runtime Transition shall declare exactly one Trigger." in content

    for trigger in TRIGGER_CLASSES:
        assert trigger in content

    assert "Undeclared triggers are prohibited." in content


def test_transition_preconditions_are_declared() -> None:
    content = normalized_text()

    for precondition in PRECONDITIONS:
        assert precondition in content

    assert "Every mandatory precondition shall succeed." in content


def test_source_state_is_exactly_one_and_preexisting() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall reference exactly one "
        "Source State.",
        "The Source State shall exist before the transition.",
        "Unknown Source States are prohibited.",
    ):
        assert requirement in content


def test_target_state_is_exactly_one_and_post_transition() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall reference exactly one "
        "Target State.",
        "The Target State shall become valid only after "
        "successful transition completion.",
        "Unknown Target States are prohibited.",
    ):
        assert requirement in content


def test_transition_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Scope.",
        "Trigger.",
        "Preconditions.",
        "Source State.",
        "Target State.",
        "Ordering.",
        "Atomicity.",
        "Determinism.",
        "Integrity.",
        "Relationships.",
        "Canonical Serialization.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_transition_ordering_is_strict_and_monotonic() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall possess exactly one "
        "deterministic Transition Sequence Number.",
        "Transition Sequence Numbers shall be strictly monotonic.",
        "Transition reordering is prohibited.",
        "Transition skipping is prohibited.",
        "Transition rollback is prohibited.",
    ):
        assert requirement in content


def test_transition_atomicity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Transition shall execute as one atomic operation.",
        "Partial Runtime Transitions are prohibited.",
        "Interrupted Runtime Transitions shall fail.",
        "Atomicity violations shall invalidate the transition.",
    ):
        assert requirement in content


def test_transition_determinism_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "The same Source State, Trigger, Preconditions, and "
        "Runtime Context shall always produce the same Target State.",
        "Implementation-defined transition behavior is prohibited.",
        "Non-deterministic transitions are prohibited.",
    ):
        assert requirement in content


def test_transition_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Transition shall possess exactly one "
        "deterministic Integrity Reference."
    ) in content

    for binding in (
        "Identity.",
        "Version.",
        "Source State.",
        "Target State.",
        "Trigger.",
        "Ordering.",
        "Relationships.",
        "Serialization.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Integrity." in content


def test_transition_traceability_is_complete() -> None:
    content = normalized_text()

    for reference in (
        "Runtime Transition Identity.",
        "Runtime State Reference.",
        "Runtime Stage Reference.",
        "Source State Reference.",
        "Target State Reference.",
        "Validation Reference.",
        "Replay Reference.",
        "Certification Reference when applicable.",
    ):
        assert reference in content

    assert "Traceability shall remain complete." in content


def test_transition_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Belong to one Runtime State.",
        "Reference one Runtime Stage.",
        "Reference one Source State.",
        "Reference one Target State.",
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
        "Every Runtime Transition shall possess one "
        "canonical serialization."
    ) in content

    for property_name in (
        "Identity.",
        "Version.",
        "Lifecycle.",
        "Trigger.",
        "Source State.",
        "Target State.",
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
        "Trigger is invalid.",
        "Preconditions fail.",
        "Source State is invalid.",
        "Target State is invalid.",
        "Ordering is invalid.",
        "Atomic execution fails.",
        "Deterministic execution cannot be verified.",
        "Relationships cannot be resolved.",
        "Canonical serialization fails.",
        "Mutation occurs after transition completion.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify Runtime Configuration.",
        "Modify Runtime Limits.",
        "Modify Runtime Execution Context.",
        "Modify Runtime Execution Request.",
        "Modify registered Facts.",
        "Modify registered Premises.",
        "Modify registered Rules.",
        "Modify CKP-005 Baseline.",
        "Repair invalid transitions.",
        "Invent missing transition state.",
    ):
        assert prohibition in content


def test_transition_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in TRANSITION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Trigger is valid.",
        "Preconditions succeed.",
        "Source State is valid.",
        "Target State is valid.",
        "Ordering is valid.",
        "Atomic execution succeeds.",
        "Deterministic execution succeeds.",
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
        "Runtime Transition Identity.",
        "Runtime Transition Version.",
        "Runtime Transition Lifecycle.",
        "Runtime Transition Scope.",
        "Runtime Transition Trigger.",
        "Runtime Transition Preconditions.",
        "Runtime Transition Source State.",
        "Runtime Transition Target State.",
        "Runtime Transition Validation.",
        "Runtime Transition Ordering.",
        "Runtime Transition Atomicity.",
        "Runtime Transition Determinism.",
        "Runtime Transition Integrity.",
        "Runtime Transition Traceability.",
        "Runtime Transition Relationships.",
        "Canonical Serialization.",
        "Failure Behavior.",
        "Read-Only Boundary.",
        "Runtime Transition Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Execution algorithms.",
        "Concrete state machines.",
        "Persistence.",
        "Write-ahead logging.",
        "Event sourcing.",
        "Schedulers.",
        "Concurrency.",
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

    assert "CKP-006.7" in content
    assert "Runtime Stage Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
