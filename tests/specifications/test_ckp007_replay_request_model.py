"""
Executable Specification

CKP-007.3
Commerce Replay Request Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_REQUEST_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Request Identity",
    "## Replay Request Version",
    "## Replay Request Lifecycle",
    "## Replay Request Status",
    "## Replay Request Scope",
    "## Historical Execution Target",
    "## Historical Artifact Requirements",
    "## Historical Environment Requirements",
    "## Baseline Pinning",
    "## Registry Pinning",
    "## Runtime Pinning",
    "## Configuration Pinning",
    "## Limits Pinning",
    "## Replay Request Inputs",
    "## Replay Request Constraints",
    "## Replay Request Preconditions",
    "## Replay Request Admission",
    "## Replay Request Validation",
    "## Replay Request Integrity",
    "## Replay Request Traceability",
    "## Replay Request Relationships",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Request Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Validated.",
    "Admitted.",
    "Executed.",
    "Completed.",
    "Archived.",
)

STATUS_VALUES = (
    "Created.",
    "Pending.",
    "Validated.",
    "Rejected.",
    "Executing.",
    "Completed.",
    "Failed.",
    "Archived.",
)

REQUIRED_INPUTS = (
    "Replay Request Identifier.",
    "Replay Request Version.",
    "Historical Runtime Execution Reference.",
    "Historical Runtime Result Reference.",
    "Historical Artifact Registry Reference.",
    "Historical Runtime Configuration Reference.",
    "Historical Runtime Limits Reference.",
    "Historical Runtime Version.",
    "Historical Runtime Structure Version.",
    "CKP-005 Baseline Reference.",
    "CKP-006 Baseline Reference.",
    "Graph Identifier.",
    "Graph Version.",
    "Registry Version References.",
    "Expected Replay Mode.",
    "Expected Comparison Policy.",
    "Expected Divergence Policy.",
    "Source Evidence References.",
    "Replay Request Integrity Reference.",
)

PRECONDITIONS = (
    "Resolved historical execution.",
    "Resolved historical artifacts.",
    "Resolved baselines.",
    "Resolved runtime version.",
    "Resolved configuration.",
    "Resolved limits.",
    "Resolved registry versions.",
    "Resolved integrity reference.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_REQUEST_IDENTITY_VIOLATION.",
    "REPLAY_REQUEST_VERSION_VIOLATION.",
    "REPLAY_REQUEST_SCOPE_VIOLATION.",
    "REPLAY_REQUEST_REFERENCE_VIOLATION.",
    "REPLAY_REQUEST_BASELINE_VIOLATION.",
    "REPLAY_REQUEST_RUNTIME_VIOLATION.",
    "REPLAY_REQUEST_CONFIGURATION_VIOLATION.",
    "REPLAY_REQUEST_LIMITS_VIOLATION.",
    "REPLAY_REQUEST_REGISTRY_VIOLATION.",
    "REPLAY_REQUEST_INTEGRITY_VIOLATION.",
    "REPLAY_REQUEST_SERIALIZATION_VIOLATION.",
    "REPLAY_REQUEST_ORDERING_VIOLATION.",
    "REPLAY_REQUEST_VALIDATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

REQUEST_INVARIANTS = (
    "Exactly one Replay Request Identity.",
    "Exactly one Replay Request Version.",
    "Exactly one Historical Runtime Execution.",
    "Exactly one Historical Runtime Result.",
    "Exactly one Historical Artifact Registry.",
    "Exactly one Runtime Version.",
    "Exactly one Runtime Configuration.",
    "Exactly one Runtime Limits reference.",
    "Exactly one Replay Result.",
    "Deterministic Ordering.",
    "Integrity Preservation.",
    "Traceability Preservation.",
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
    assert "Title Commerce Replay Request Model" in content
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


def test_no_unexpected_level_two_headings_exist() -> None:
    assert tuple(level_two_headings()) == EXPECTED_SECTIONS


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, and integrity-preserving "
        "Replay Request.",
        "Replay Request defines the unique normative entry "
        "point of exactly one Replay operation.",
        "Replay Request identifies one historical Runtime "
        "Execution to reconstruct.",
        "Replay Request fixes every normative reference "
        "required to reproduce the selected historical execution.",
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
    ):
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_request_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Request shall possess exactly one "
        "immutable Replay Request Identifier.",
        "CKP-REPLAY-REQUEST-000001",
        "Replay Request Identity shall be globally unique.",
        "Replay Request Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Request Identity shall fail validation.",
    ):
        assert requirement in content


def test_request_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Request shall declare exactly one Version.",
        "Version identifies the Replay Request schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_request_lifecycle_is_declared() -> None:
    content = normalized_text()

    for state in LIFECYCLE_STATES:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_request_status_is_closed_and_deterministic() -> None:
    content = normalized_text()

    assert "Replay Request Status shall be exactly one of:" in content

    for status in STATUS_VALUES:
        assert status in content

    assert "Replay Request Status shall be deterministic." in content


def test_request_scope_is_exactly_one_historical_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Replay Request shall identify exactly one "
        "historical Runtime Execution.",
        "Replay Request shall never reference multiple "
        "historical executions.",
        "Replay Request Scope shall remain immutable.",
    ):
        assert requirement in content


def test_historical_execution_target_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request shall reference exactly one "
        "Historical Runtime Execution.",
        "Historical Runtime Execution Reference shall "
        "remain immutable.",
        "Historical Runtime Result Reference shall be mandatory.",
    ):
        assert requirement in content


def test_historical_artifact_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Historical Artifact Registry Reference.",
        "Source Evidence References.",
        "Historical artifacts shall be versioned.",
        "Historical artifacts shall remain immutable.",
    ):
        assert requirement in content


def test_historical_environment_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Historical Runtime Configuration Reference.",
        "Historical Runtime Limits Reference.",
        "Historical Runtime Version.",
        "Historical Runtime Structure Version.",
        "Historical environment shall remain pinned.",
    ):
        assert requirement in content


def test_baseline_pinning_is_explicit_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-005 Baseline Reference.",
        "CKP-006 Baseline Reference.",
        "Pinned baselines shall remain immutable.",
        "Baseline mismatch shall fail validation.",
    ):
        assert requirement in content


def test_registry_pinning_is_explicit_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Registry Version References.",
        "Pinned registries shall remain immutable.",
        "Registry mismatch shall fail validation.",
    ):
        assert requirement in content


def test_runtime_pinning_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request shall pin exactly one Historical "
        "Runtime Version.",
        "Runtime version shall remain immutable.",
        "Runtime mismatch shall fail validation.",
    ):
        assert requirement in content


def test_configuration_pinning_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request shall pin exactly one Historical "
        "Runtime Configuration Reference.",
        "Pinned configuration shall remain immutable.",
        "Configuration mismatch shall fail validation.",
    ):
        assert requirement in content


def test_limits_pinning_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request shall pin exactly one Historical "
        "Runtime Limits Reference.",
        "Pinned limits shall remain immutable.",
        "Limits mismatch shall fail validation.",
    ):
        assert requirement in content


def test_all_mandatory_inputs_are_declared() -> None:
    content = normalized_text()

    for required_input in REQUIRED_INPUTS:
        assert required_input in content

    assert "Every mandatory input shall be present." in content


def test_request_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Replay Request shall reference exactly one "
        "historical execution.",
        "Replay Request shall preserve deterministic ordering.",
        "Replay Request shall preserve immutable references.",
        "Replay Request shall preserve version consistency.",
        "Replay Request shall preserve traceability.",
    ):
        assert constraint in content


def test_request_preconditions_are_declared() -> None:
    content = normalized_text()

    for precondition in PRECONDITIONS:
        assert precondition in content

    assert "Every precondition shall succeed." in content


def test_request_admission_is_deterministic_and_fail_closed() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request shall be admitted only when all "
        "preconditions succeed.",
        "Admission shall be deterministic.",
        "Admission shall fail closed.",
        "Rejected Replay Requests shall not execute.",
    ):
        assert requirement in content


def test_request_validation_is_complete_and_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Identity.",
        "Version.",
        "Scope.",
        "Historical references.",
        "Pinned baselines.",
        "Pinned runtime.",
        "Pinned configuration.",
        "Pinned limits.",
        "Pinned registries.",
        "Integrity reference.",
        "Canonical serialization.",
        "Deterministic ordering.",
    ):
        assert validation_check in content

    assert "Replay Request Validation shall fail closed." in content


def test_request_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "References.",
        "Pinned versions.",
        "Canonical serialization.",
        "Deterministic ordering.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert (
        "Mutation shall invalidate Replay Request Integrity."
    ) in content


def test_request_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Historical Runtime Execution.",
        "Historical Runtime Result.",
        "Historical Artifact Registry.",
        "Historical Runtime Configuration.",
        "Historical Runtime Limits.",
        "Frozen Baselines.",
        "Replay Evidence.",
        "Replay Result.",
    ):
        assert traceability_target in content


def test_request_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Request belongs to exactly one Replay Instance.",
        "Replay Request targets exactly one Historical "
        "Runtime Execution.",
        "Replay Request references exactly one Historical "
        "Runtime Result.",
        "Replay Request references exactly one Historical "
        "Artifact Registry.",
        "Replay Request produces exactly one Replay Result.",
        "Relationships shall remain deterministic.",
        "Relationships shall remain resolvable.",
    ):
        assert relationship in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Request shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "References.",
        "Pinned versions.",
        "Ordering.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Request ordering shall be deterministic.",
        "Equivalent Replay Requests shall produce equivalent ordering.",
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
        "Replay Request Identity is invalid.",
        "Replay Request Version is unsupported.",
        "Replay Request Scope is violated.",
        "Historical execution cannot be resolved.",
        "Historical artifacts cannot be resolved.",
        "Baseline pinning fails.",
        "Runtime pinning fails.",
        "Configuration pinning fails.",
        "Limits pinning fails.",
        "Registry pinning fails.",
        "Integrity verification fails.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
    ):
        assert condition in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    for historical_target in (
        "Historical Runtime Execution.",
        "Historical Runtime Result.",
        "Historical Artifact Registry.",
        "Historical Runtime Configuration.",
        "Historical Runtime Limits.",
        "Historical Evidence.",
        "Frozen Baselines.",
        "Historical references.",
    ):
        assert historical_target in content

    assert "Replay Request shall not modify:" in content


def test_request_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in REQUEST_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Scope is valid.",
        "Historical execution resolves.",
        "Historical artifacts resolve.",
        "Pinned baselines resolve.",
        "Pinned runtime resolves.",
        "Pinned configuration resolves.",
        "Pinned limits resolve.",
        "Pinned registries resolve.",
        "Integrity is preserved.",
        "Deterministic ordering succeeds.",
        "Validation succeeds.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Request Identity.",
        "Replay Request Version.",
        "Replay Request Lifecycle.",
        "Replay Request Status.",
        "Replay Request Scope.",
        "Historical references.",
        "Pinning model.",
        "Inputs.",
        "Constraints.",
        "Preconditions.",
        "Admission.",
        "Validation.",
        "Integrity.",
        "Traceability.",
        "Relationships.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Historical Boundary.",
        "Replay Request Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Reconstruction algorithms.",
        "Comparison algorithms.",
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
        "Future CKP-007 specifications shall preserve "
        "this Replay Request Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.4" in content
    assert "Replay Environment Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
