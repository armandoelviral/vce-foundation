"""
Executable Specification

CKP-007.18
Commerce Replay Failure Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_FAILURE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Failure Identity",
    "## Replay Failure Version",
    "## Replay Failure Lifecycle",
    "## Replay Failure Scope",
    "## Replay Failure Inputs",
    "## Replay Failure Preconditions",
    "## Replay Attestation Reference",
    "## Failure Identity",
    "## Failure Classification",
    "## Failure Status",
    "## Failure Condition",
    "## Failure Source",
    "## Failure Stage",
    "## Failure Causality",
    "## Failure Evidence",
    "## Failure Integrity",
    "## Failure Traceability",
    "## Failure Relationships",
    "## Failure Ordering",
    "## Failure Completeness",
    "## Failure Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Failure Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Detected.",
    "Recorded.",
    "Archived.",
)

FAILURE_STATUSES = (
    "Open.",
    "Confirmed.",
    "Terminal.",
)

REQUIRED_INPUTS = (
    "Replay Failure Identifier.",
    "Replay Failure Version.",
    "Replay Attestation Reference.",
    "Replay Certification Reference.",
    "Replay Validation Reference.",
    "Replay Result Reference.",
    "Failure Identifier.",
    "Failure Classification.",
    "Failure Status.",
    "Failure Condition.",
    "Failure Source.",
    "Failure Stage.",
    "Failure Causality.",
    "Failure Evidence Reference.",
    "Failure Integrity Reference.",
    "Failure Traceability Reference.",
    "Replay Failure Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Attestation.",
    "Validated Replay Validation.",
    "Resolved Replay Result.",
    "Verified Replay Integrity.",
    "Verified Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Failure shall preserve exactly one Replay.",
    "Replay Failure shall require exactly one Replay Attestation.",
    "Replay Failure shall preserve Replay Validation.",
    "Replay Failure shall preserve Replay Integrity.",
    "Replay Failure shall preserve Replay Traceability.",
    "Replay Failure shall preserve Failure Evidence.",
    "Replay Failure shall preserve Failure Causality.",
    "Replay Failure shall be deterministic.",
    "Replay Failure shall remain immutable.",
    "Replay Failure shall fail closed.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_FAILURE_IDENTITY_VIOLATION.",
    "REPLAY_FAILURE_VERSION_VIOLATION.",
    "REPLAY_FAILURE_LIFECYCLE_VIOLATION.",
    "REPLAY_FAILURE_SCOPE_VIOLATION.",
    "REPLAY_FAILURE_INPUT_VIOLATION.",
    "REPLAY_FAILURE_PRECONDITION_VIOLATION.",
    "REPLAY_FAILURE_REFERENCE_VIOLATION.",
    "FAILURE_IDENTITY_VIOLATION.",
    "FAILURE_CLASSIFICATION_VIOLATION.",
    "FAILURE_STATUS_VIOLATION.",
    "FAILURE_CONDITION_VIOLATION.",
    "FAILURE_SOURCE_VIOLATION.",
    "FAILURE_STAGE_VIOLATION.",
    "FAILURE_CAUSALITY_VIOLATION.",
    "FAILURE_EVIDENCE_VIOLATION.",
    "FAILURE_INTEGRITY_VIOLATION.",
    "FAILURE_TRACEABILITY_VIOLATION.",
    "FAILURE_RELATIONSHIP_VIOLATION.",
    "FAILURE_ORDERING_VIOLATION.",
    "FAILURE_COMPLETENESS_VIOLATION.",
    "FAILURE_CONSISTENCY_VIOLATION.",
    "REPLAY_FAILURE_SERIALIZATION_VIOLATION.",
    "REPLAY_FAILURE_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Failure Identity is invalid.",
    "Replay Failure Version is unsupported.",
    "Mandatory inputs are missing.",
    "Mandatory references cannot be resolved.",
    "Replay Attestation cannot be resolved.",
    "Replay Validation cannot be resolved.",
    "Replay Result cannot be resolved.",
    "Failure Evidence cannot be resolved.",
    "Failure Integrity verification fails.",
    "Failure Traceability verification fails.",
    "Failure Classification is invalid.",
    "Failure Status is invalid.",
    "Failure Condition is missing.",
    "Failure Source is missing.",
    "Failure Stage is missing.",
    "Failure Causality is missing.",
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
    "Historical Replay Attestation.",
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Failure Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Attestation.",
    "Exactly one Failure Classification.",
    "Exactly one Failure Status.",
    "Exactly one Replay Failure Integrity Reference.",
    "Identity Preservation.",
    "Attestation Preservation.",
    "Failure Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Failure.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Attestation resolves successfully.",
    "Replay Validation resolves successfully.",
    "Replay Result resolves successfully.",
    "Failure Classification is valid.",
    "Failure Status is valid.",
    "Failure Condition is complete.",
    "Failure Source is consistent.",
    "Failure Stage is consistent.",
    "Failure Causality is preserved.",
    "Failure Evidence is resolved.",
    "Failure Integrity is verified.",
    "Failure Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Failure Identity.",
    "Replay Failure Version.",
    "Replay Failure Lifecycle.",
    "Replay Failure Scope.",
    "Replay Failure Inputs.",
    "Replay Failure Preconditions.",
    "Replay Attestation Reference.",
    "Failure Identity.",
    "Failure Classification.",
    "Failure Status.",
    "Failure Condition.",
    "Failure Source.",
    "Failure Stage.",
    "Failure Causality.",
    "Failure Evidence.",
    "Failure Integrity.",
    "Failure Traceability.",
    "Failure Relationships.",
    "Failure Ordering.",
    "Failure Completeness.",
    "Failure Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Failure Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Replay engine.",
    "Recovery engine.",
    "Retry engine.",
    "Remediation engine.",
    "Persistence.",
    "WAL.",
    "Event sourcing.",
    "Scheduler.",
    "Concurrency.",
    "Distributed infrastructure.",
    "Cryptographic algorithms.",
    "PKI.",
    "HSM.",
    "Storage.",
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
    assert "Title Commerce Replay Failure Model" in content
    assert "Abbreviation CRFM" in content
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

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "No additional lifecycle states shall be defined" in content
    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_failure_statuses_are_exact() -> None:
    content = normalized_text()

    for failure_status in FAILURE_STATUSES:
        assert failure_status in content

    assert (
        "Lifecycle and Failure Status shall remain independent "
        "normative concepts."
    ) in content


def test_all_required_inputs_are_declared() -> None:
    content = normalized_text()

    for required_input in REQUIRED_INPUTS:
        assert required_input in content

    assert "Every mandatory input shall be present." in content


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


def test_replay_attestation_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Failure shall reference exactly one immutable "
        "Replay Attestation.",
        "Replay Attestation Reference shall remain resolvable.",
        "Replay Attestation Reference shall remain immutable.",
        "Replay Attestation Reference shall preserve "
        "attestation traceability.",
        "Missing Replay Attestation Reference shall fail validation.",
        "Unresolved Replay Attestation Reference shall fail validation.",
    ):
        assert requirement in content


def test_failure_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Failure shall possess exactly one immutable "
        "Failure Identifier.",
        "Failure Identity shall be globally unique.",
        "Failure Identity shall never be reused.",
        "Missing Failure Identifier shall fail validation.",
        "Malformed Failure Identifier shall fail validation.",
        "Duplicated Failure Identifier shall fail validation.",
    ):
        assert requirement in content


def test_failure_classification_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Failure shall declare exactly one "
        "Failure Classification.",
        "Failure Classification identifies the normative category "
        "of the Replay Failure.",
        "Failure Classification shall remain immutable.",
        "Missing Failure Classification shall fail validation.",
        "Unsupported Failure Classification shall fail validation.",
    ):
        assert requirement in content


def test_failure_status_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Replay Failure shall declare exactly one Failure Status."
        in content
    )

    for status in FAILURE_STATUSES:
        assert status in content

    assert (
        "Failure Status shall remain immutable after terminal completion."
        in content
    )
    assert "Unsupported Failure Status shall fail validation." in content


def test_failure_condition_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Failure shall declare exactly one Failure Condition.",
        "Failure Condition shall describe the normative condition "
        "responsible for the Replay Failure.",
        "Failure Condition shall remain immutable.",
        "Missing Failure Condition shall fail validation.",
    ):
        assert requirement in content


def test_failure_source_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Failure shall declare exactly one Failure Source.",
        "Failure Source identifies the origin responsible for the "
        "detected Replay Failure.",
        "Failure Source shall remain immutable.",
        "Missing Failure Source shall fail validation.",
    ):
        assert requirement in content


def test_failure_stage_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Failure shall declare exactly one Failure Stage.",
        "Failure Stage identifies the Replay Stage where the Failure occurred.",
        "Failure Stage shall remain immutable.",
        "Failure Stage shall preserve historical ordering.",
        "Missing Failure Stage shall fail validation.",
    ):
        assert requirement in content


def test_failure_causality_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Failure shall declare exactly one Failure Causality.",
        "Failure Causality shall identify the causal relationship "
        "explaining the Replay Failure.",
        "Failure Causality shall remain immutable.",
        "Missing Failure Causality shall fail validation.",
    ):
        assert requirement in content


def test_failure_evidence_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Failure shall reference exactly one Failure Evidence.",
        "Failure Evidence shall preserve the historical evidence "
        "supporting the Replay Failure.",
        "Failure Evidence shall remain immutable.",
        "Failure Evidence shall remain completely traceable.",
        "Missing Failure Evidence shall fail validation.",
        "Unresolved Failure Evidence shall fail validation.",
    ):
        assert requirement in content


def test_failure_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Failure shall possess exactly one deterministic "
        "Failure Integrity Reference."
    ) in content

    for binding in (
        "Failure Identity.",
        "Replay Failure Identity.",
        "Failure Classification.",
        "Failure Status.",
        "Failure Condition.",
        "Failure Source.",
        "Failure Stage.",
        "Failure Causality.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Failure Integrity." in content
    assert "Failure Integrity shall remain immutable." in content


def test_failure_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Replay Attestation.",
        "Replay Validation.",
        "Replay Result.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Failure Evidence.",
        "Failure Causality.",
    ):
        assert traceability_target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_failure_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Failure belongs to exactly one Replay.",
        "Replay Failure references exactly one Replay Attestation.",
        "Replay Failure references exactly one Replay Validation.",
        "Replay Failure references exactly one Replay Result.",
        "Replay Failure references exactly one Failure Evidence.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_failure_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Failure Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent Failure Ordering.",
        "Implementation-defined ordering is prohibited.",
        "Failure Ordering shall remain immutable.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_failure_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Failure shall preserve all mandatory Failure information.",
        "Replay Failure shall preserve all mandatory references.",
        "Replay Failure shall preserve all mandatory traceability.",
        "Partial Replay Failure shall fail validation.",
        "Missing mandatory Failure information shall fail validation.",
    ):
        assert requirement in content


def test_failure_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Attestation.",
        "Replay Validation.",
        "Replay Result.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Failure Evidence.",
        "Failure Causality.",
        "Failure Classification.",
        "Failure Status.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Failure shall never reinterpret preserved Replay artifacts.",
        "Replay Failure shall never normalize preserved information.",
        "Replay Failure shall never repair preserved information.",
        "Replay Failure shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Failure shall possess exactly one canonical serialization."
        in content
    )

    for preserved_property in (
        "Replay Failure Identity.",
        "Replay Failure Version.",
        "Failure Identity.",
        "Failure Classification.",
        "Failure Status.",
        "Failure Condition.",
        "Failure Source.",
        "Failure Stage.",
        "Failure Causality.",
        "Failure Evidence.",
        "Failure Integrity.",
        "Failure Traceability.",
        "Replay Attestation Reference.",
        "Replay Validation Reference.",
        "Replay Result Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Failure Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Failure Ordering.",
        "Equivalent Replay Failures shall produce identical ordering.",
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

    assert "Replay Failure shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Failure shall never modify, reinterpret, normalize, "
        "repair, replace, merge, or suppress historical artifacts."
    ) in content

    assert (
        "Replay Failure shall preserve the original historical "
        "information exactly as recorded."
    ) in content


def test_replay_failure_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Failure shall remain immutable throughout "
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
        "Replay Failure Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.19" in content
    assert "Replay Result Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
