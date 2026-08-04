"""
Executable Specification

CKP-006.8
Commerce Runtime Artifact Registry Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_RUNTIME_ARTIFACT_REGISTRY_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Artifact Registry Identity",
    "## Artifact Registry Version",
    "## Artifact Registry Lifecycle",
    "## Artifact Registry Scope",
    "## Artifact Registry Properties",
    "## Artifact Identity",
    "## Artifact Type",
    "## Artifact Lifecycle",
    "## Artifact Classification",
    "## Artifact Source",
    "## Artifact Ownership",
    "## Artifact Registration",
    "## Artifact Resolution",
    "## Artifact References",
    "## Artifact Relationships",
    "## Artifact Provenance",
    "## Artifact Evidence",
    "## Artifact Integrity",
    "## Artifact Immutability",
    "## Artifact Registry Closure",
    "## Artifact Registry Validation",
    "## Artifact Registry Integrity",
    "## Artifact Registry Traceability",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Artifact Registry Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

REGISTRY_LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Active.",
    "Closed.",
    "Archived.",
)

ARTIFACT_TYPES = (
    "Runtime Inputs.",
    "Execution Request.",
    "Execution Context.",
    "Runtime Configuration.",
    "Runtime Limits.",
    "Runtime State.",
    "Runtime Stages.",
    "Runtime Transitions.",
    "Facts.",
    "Premises.",
    "Rules.",
    "Rule Applications.",
    "Variable Bindings.",
    "Derived Conclusions.",
    "Proofs.",
    "Reasoning Evidence.",
    "Runtime Evidence.",
    "Explanation.",
    "Validation Artifacts.",
    "Certification Artifacts.",
    "Failure Artifacts.",
    "Runtime Outputs.",
    "Runtime Result.",
    "Replay Descriptor.",
)

FAILURE_CLASSIFICATIONS = (
    "ARTIFACT_REGISTRY_IDENTITY_VIOLATION.",
    "ARTIFACT_REGISTRY_VERSION_VIOLATION.",
    "ARTIFACT_IDENTITY_VIOLATION.",
    "ARTIFACT_TYPE_VIOLATION.",
    "ARTIFACT_REGISTRATION_VIOLATION.",
    "ARTIFACT_RESOLUTION_VIOLATION.",
    "ARTIFACT_RELATIONSHIP_VIOLATION.",
    "ARTIFACT_PROVENANCE_VIOLATION.",
    "ARTIFACT_EVIDENCE_VIOLATION.",
    "ARTIFACT_INTEGRITY_VIOLATION.",
    "ARTIFACT_IMMUTABILITY_VIOLATION.",
    "ARTIFACT_REGISTRY_CLOSURE_VIOLATION.",
    "ARTIFACT_REGISTRY_VALIDATION_VIOLATION.",
    "ARTIFACT_REGISTRY_SERIALIZATION_VIOLATION.",
    "ARTIFACT_REGISTRY_ORDERING_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

REGISTRY_INVARIANTS = (
    "Exactly one Registry Identity.",
    "Exactly one Registry Version.",
    "Exactly one Runtime Execution.",
    "Exactly one registration per Artifact.",
    "Deterministic Resolution.",
    "Deterministic Serialization.",
    "Deterministic Ordering.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Registry Closure Preservation.",
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
    assert "Title Commerce Runtime Artifact Registry Model" in content
    assert "Abbreviation CRARM" in content
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
        "integrity-preserving Runtime Artifact Registry "
        "governing every artifact consumed, produced, derived, "
        "or referenced during exactly one Runtime Execution.",
        "The Runtime Artifact Registry represents the "
        "authoritative catalog of Runtime artifacts.",
        "This specification defines registry identity, lifecycle, "
        "scope, artifact identity, classification, ownership, "
        "registration, resolution, provenance, evidence, integrity, "
        "immutability, validation, traceability, serialization, "
        "deterministic ordering, failure semantics, and structural "
        "invariants.",
    ):
        assert requirement in content


def test_non_implementation_boundaries_are_declared() -> None:
    content = normalized_text()

    for boundary in (
        "It does not define registry implementation.",
        "It does not define database schemas.",
        "It does not define persistence.",
        "It does not define WAL.",
        "It does not define event sourcing.",
        "It does not define filesystem layout.",
        "It does not define object storage.",
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
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_registry_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Artifact Registry shall possess exactly "
        "one immutable Artifact Registry Identifier.",
        "CKP-RUNTIME-ARTIFACT-REGISTRY-000001",
        "Artifact Registry Identity shall be globally unique.",
        "Artifact Registry Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Artifact "
        "Registry Identity shall fail validation.",
    ):
        assert requirement in content


def test_registry_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Runtime Artifact Registry shall declare exactly "
        "one Version.",
        "Version identifies the Artifact Registry schema.",
        "Version shall remain independent of Identity.",
        "Unsupported versions shall fail validation.",
    ):
        assert requirement in content


def test_registry_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle in REGISTRY_LIFECYCLE_STATES:
        assert lifecycle in content

    assert "Terminal lifecycle states shall remain immutable." in content
    assert "Lifecycle regression is prohibited." in content


def test_registry_scope_is_exactly_one_execution() -> None:
    content = normalized_text()

    for requirement in (
        "One Runtime Artifact Registry shall belong to exactly "
        "one Runtime Execution.",
        "Artifact Registry sharing across Runtime Executions "
        "is prohibited.",
    ):
        assert requirement in content


def test_registry_properties_are_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Registry Identifier.",
        "Registry Version.",
        "Lifecycle.",
        "Execution Reference.",
        "Integrity Reference.",
        "Traceability Reference.",
        "Canonical Serialization Reference.",
    ):
        assert property_name in content


def test_artifact_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every registered Artifact shall possess exactly one "
        "immutable Artifact Identifier.",
        "Artifact Identity shall be globally unique.",
        "Artifact Identity shall never be reused.",
    ):
        assert requirement in content


def test_all_required_artifact_types_are_declared() -> None:
    content = normalized_text()

    assert "Every Artifact shall declare exactly one Artifact Type." in content

    for artifact_type in ARTIFACT_TYPES:
        assert artifact_type in content

    assert "Undeclared Artifact Types are prohibited." in content


def test_artifact_lifecycle_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall declare exactly one Lifecycle.",
        "Lifecycle transitions shall be deterministic.",
        "Terminal lifecycle states shall remain immutable.",
    ):
        assert requirement in content


def test_artifact_classification_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall declare exactly one Classification.",
        "Classification shall remain immutable after registration.",
    ):
        assert requirement in content


def test_artifact_source_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall reference exactly one Source.",
        "Unknown sources are prohibited.",
    ):
        assert requirement in content


def test_artifact_ownership_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall possess exactly one Owner.",
        "Ownership shall remain immutable.",
    ):
        assert requirement in content


def test_artifact_registration_is_exactly_once() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall be registered exactly once.",
        "Duplicate registrations are prohibited.",
        "Registration shall preserve Identity.",
        "Registration shall preserve Integrity.",
    ):
        assert requirement in content


def test_artifact_resolution_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Every registered Artifact shall be deterministically "
        "resolvable.",
        "Resolution ambiguity is prohibited.",
        "Unresolved Artifacts shall fail validation.",
    ):
        assert requirement in content


def test_artifact_references_are_closed() -> None:
    content = normalized_text()

    for requirement in (
        "Artifacts may reference other registered Artifacts.",
        "All references shall resolve deterministically.",
        "Dangling references are prohibited.",
    ):
        assert requirement in content


def test_artifact_relationships_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Relationships between Artifacts shall be explicit.",
        "Relationships shall be deterministic.",
        "Relationships shall preserve integrity.",
        "Relationships shall preserve traceability.",
    ):
        assert requirement in content


def test_artifact_provenance_is_complete_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall preserve complete Provenance.",
        "Provenance shall remain immutable.",
    ):
        assert requirement in content


def test_artifact_evidence_is_resolvable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Artifact shall preserve its supporting Evidence.",
        "Evidence references shall remain resolvable.",
    ):
        assert requirement in content


def test_artifact_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Artifact shall possess exactly one deterministic "
        "Integrity Reference."
    ) in content
    assert "Mutation shall invalidate Integrity." in content


def test_registered_artifacts_are_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Registered Artifacts shall become immutable after "
        "successful registration.",
        "Mutation of registered Artifacts is prohibited.",
    ):
        assert requirement in content


def test_registry_closure_is_complete() -> None:
    content = normalized_text()

    for requirement in (
        "Runtime Artifact Registry closure shall occur only "
        "after all mandatory Runtime Artifacts have been "
        "registered or deterministically accounted for.",
        "Incomplete Runtime Artifact Registries shall fail validation.",
    ):
        assert requirement in content


def test_registry_validation_is_fail_closed() -> None:
    content = normalized_text()

    for validation_check in (
        "Registry Identity.",
        "Registry Version.",
        "Lifecycle.",
        "Scope.",
        "Artifact Identity.",
        "Artifact Type.",
        "Artifact Registration.",
        "Artifact Resolution.",
        "Artifact Relationships.",
        "Artifact Provenance.",
        "Artifact Evidence.",
        "Artifact Integrity.",
        "Artifact Immutability.",
        "Registry Closure.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
    ):
        assert validation_check in content

    assert "Validation shall fail closed." in content


def test_registry_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Artifact Registry shall possess exactly "
        "one deterministic Integrity Reference."
    ) in content

    for binding in (
        "Registry Identity.",
        "Registry Version.",
        "Registered Artifacts.",
        "Relationships.",
        "Serialization.",
        "Ordering.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Registry Integrity." in content


def test_registry_traceability_is_complete() -> None:
    content = normalized_text()

    for reference in (
        "Registry Identity.",
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


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Runtime Artifact Registry shall possess one "
        "canonical serialization."
    ) in content

    for property_name in (
        "Registry Identity.",
        "Registry Version.",
        "Registered Artifacts.",
        "Relationships.",
        "Integrity.",
    ):
        assert property_name in content

    assert "Canonical serialization shall be deterministic." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Artifacts shall possess one canonical ordering.",
        "Registration ordering shall be deterministic.",
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
        "Registry Identity is invalid.",
        "Registry Version is unsupported.",
        "Artifact Identity is invalid.",
        "Artifact Type is invalid.",
        "Registration is duplicated.",
        "Artifact resolution fails.",
        "Relationships cannot be resolved.",
        "Evidence cannot be resolved.",
        "Integrity verification fails.",
        "Registry Closure is incomplete.",
        "Canonical serialization fails.",
        "Deterministic ordering fails.",
        "Mutation occurs after registration.",
    ):
        assert condition in content


def test_read_only_boundary_is_strict() -> None:
    content = normalized_text()

    for requirement in (
        "The Runtime Artifact Registry shall index artifacts.",
        "The Runtime Artifact Registry shall not create, repair, "
        "reinterpret, or mutate registered artifacts.",
        "The Runtime Artifact Registry shall not modify Runtime State.",
        "The Runtime Artifact Registry shall not modify "
        "Runtime Configuration.",
        "The Runtime Artifact Registry shall not modify "
        "Runtime Execution Context.",
        "The Runtime Artifact Registry shall not modify "
        "CKP-005 Baseline.",
    ):
        assert requirement in content


def test_registry_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in REGISTRY_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Registry Identity is valid.",
        "Registry Version is supported.",
        "Artifact registration is complete.",
        "Artifact resolution succeeds.",
        "Relationships resolve.",
        "Evidence resolves.",
        "Registry Closure succeeds.",
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
        "Artifact Registry Identity.",
        "Artifact Registry Version.",
        "Artifact Registry Lifecycle.",
        "Artifact Registry Scope.",
        "Artifact Registry Properties.",
        "Artifact Identity.",
        "Artifact Type.",
        "Artifact Lifecycle.",
        "Artifact Classification.",
        "Artifact Source.",
        "Artifact Ownership.",
        "Artifact Registration.",
        "Artifact Resolution.",
        "Artifact References.",
        "Artifact Relationships.",
        "Artifact Provenance.",
        "Artifact Evidence.",
        "Artifact Integrity.",
        "Artifact Immutability.",
        "Artifact Registry Closure.",
        "Artifact Registry Validation.",
        "Artifact Registry Integrity.",
        "Artifact Registry Traceability.",
        "Canonical Serialization.",
        "Deterministic Ordering.",
        "Failure Behavior.",
        "Read-Only Boundary.",
        "Artifact Registry Invariants.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Registry implementation.",
        "Database schemas.",
        "Persistence.",
        "Write-ahead logging.",
        "Event sourcing.",
        "Filesystem layout.",
        "Object storage.",
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

    assert "CKP-006.9" in content
    assert "Runtime Result Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
