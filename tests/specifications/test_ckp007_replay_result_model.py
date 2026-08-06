"""
Executable Specification

CKP-007.19
Commerce Replay Result Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_RESULT_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Result Identity",
    "## Replay Result Version",
    "## Replay Result Lifecycle",
    "## Replay Result Scope",
    "## Replay Result Inputs",
    "## Replay Result Preconditions",
    "## Replay Reconstruction Reference",
    "## Replay Comparison Reference",
    "## Replay Divergence Reference",
    "## Replay Validation Reference",
    "## Replay Certification Reference",
    "## Replay Evidence Reference",
    "## Replay Attestation Reference",
    "## Replay Failure Reference",
    "## Replay Result Status",
    "## Replay Result Outcome",
    "## Equivalence Status",
    "## Divergence Status",
    "## Result Evidence",
    "## Result Integrity",
    "## Result Traceability",
    "## Result Relationships",
    "## Result Ordering",
    "## Result Completeness",
    "## Result Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Result Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Completed.",
    "Archived.",
)

RESULT_STATUSES = (
    "COMPLETED.",
    "FAILED.",
    "CANCELLED.",
)

RESULT_OUTCOMES = (
    "EQUIVALENT.",
    "DIVERGENT.",
    "INVALID.",
    "FAILED.",
    "CANCELLED.",
)

EQUIVALENCE_STATUSES = (
    "EQUIVALENT.",
    "NON-EQUIVALENT.",
    "UNKNOWN.",
)

DIVERGENCE_STATUSES = (
    "NONE.",
    "PRESENT.",
    "UNKNOWN.",
)

REQUIRED_INPUTS = (
    "Replay Result Identifier.",
    "Replay Result Version.",
    "Replay Reconstruction Reference.",
    "Replay Comparison Reference.",
    "Replay Divergence Reference.",
    "Replay Validation Reference.",
    "Replay Certification Reference.",
    "Replay Evidence Reference.",
    "Replay Attestation Reference.",
    "Replay Failure Reference.",
    "Replay Result Status.",
    "Replay Result Outcome.",
    "Equivalence Status.",
    "Divergence Status.",
    "Result Evidence Reference.",
    "Result Integrity Reference.",
    "Result Traceability Reference.",
    "Replay Result Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Reconstruction.",
    "Validated Replay Comparison.",
    "Validated Replay Validation.",
    "Resolved Replay Integrity.",
    "Resolved Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Result shall represent exactly one Replay.",
    "Replay Result shall produce exactly one terminal status.",
    "Replay Result shall produce exactly one outcome.",
    "Replay Result shall preserve Replay Reconstruction.",
    "Replay Result shall preserve Replay Comparison.",
    "Replay Result shall preserve Replay Validation.",
    "Replay Result shall preserve Replay Integrity.",
    "Replay Result shall preserve Replay Traceability.",
    "Replay Result shall be deterministic.",
    "Replay Result shall remain immutable.",
    "Replay Result shall fail closed.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_RESULT_IDENTITY_VIOLATION.",
    "REPLAY_RESULT_VERSION_VIOLATION.",
    "REPLAY_RESULT_LIFECYCLE_VIOLATION.",
    "REPLAY_RESULT_SCOPE_VIOLATION.",
    "REPLAY_RESULT_INPUT_VIOLATION.",
    "REPLAY_RESULT_PRECONDITION_VIOLATION.",
    "REPLAY_RESULT_REFERENCE_VIOLATION.",
    "REPLAY_RESULT_STATUS_VIOLATION.",
    "REPLAY_RESULT_OUTCOME_VIOLATION.",
    "EQUIVALENCE_STATUS_VIOLATION.",
    "DIVERGENCE_STATUS_VIOLATION.",
    "RESULT_EVIDENCE_VIOLATION.",
    "RESULT_INTEGRITY_VIOLATION.",
    "RESULT_TRACEABILITY_VIOLATION.",
    "RESULT_RELATIONSHIP_VIOLATION.",
    "RESULT_ORDERING_VIOLATION.",
    "RESULT_COMPLETENESS_VIOLATION.",
    "RESULT_CONSISTENCY_VIOLATION.",
    "REPLAY_RESULT_SERIALIZATION_VIOLATION.",
    "REPLAY_RESULT_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Result Identity is invalid.",
    "Replay Result Version is unsupported.",
    "Mandatory inputs are missing.",
    "Mandatory references cannot be resolved.",
    "Replay Reconstruction cannot be resolved.",
    "Replay Comparison cannot be resolved.",
    "Replay Validation cannot be resolved.",
    "Result Evidence cannot be resolved.",
    "Replay Result Status is invalid.",
    "Replay Result Outcome is invalid.",
    "Equivalence Status is invalid.",
    "Divergence Status is invalid.",
    "Result Integrity verification fails.",
    "Result Traceability verification fails.",
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
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Result Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Result Status.",
    "Exactly one Replay Result Outcome.",
    "Exactly one Replay Result Integrity Reference.",
    "Identity Preservation.",
    "Result Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Result.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Reconstruction resolves successfully.",
    "Replay Comparison resolves successfully.",
    "Replay Validation resolves successfully.",
    "Replay Result Status is valid.",
    "Replay Result Outcome is valid.",
    "Equivalence Status is valid.",
    "Divergence Status is valid.",
    "Result Evidence is resolved.",
    "Result Integrity is verified.",
    "Result Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Result Identity.",
    "Replay Result Version.",
    "Replay Result Lifecycle.",
    "Replay Result Scope.",
    "Replay Result Inputs.",
    "Replay Result Preconditions.",
    "Replay Reconstruction Reference.",
    "Replay Comparison Reference.",
    "Replay Validation Reference.",
    "Replay Certification Reference.",
    "Replay Evidence Reference.",
    "Replay Attestation Reference.",
    "Replay Failure Reference.",
    "Replay Result Status.",
    "Replay Result Outcome.",
    "Equivalence Status.",
    "Divergence Status.",
    "Result Evidence.",
    "Result Integrity.",
    "Result Traceability.",
    "Result Relationships.",
    "Result Ordering.",
    "Result Completeness.",
    "Result Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Result Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Replay engine.",
    "Execution engine.",
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
    assert "Title Commerce Replay Result Model" in content
    assert "Abbreviation CRRM" in content
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


def test_result_statuses_are_exact() -> None:
    content = normalized_text()

    assert (
        "Every Replay Result shall declare exactly one Replay Result Status."
        in content
    )

    for status in RESULT_STATUSES:
        assert status in content

    assert "Unsupported Replay Result Status shall fail validation." in content
    assert (
        "Replay Result Lifecycle and Replay Result Status shall remain "
        "independent normative concepts."
    ) in content


def test_result_outcomes_are_exact() -> None:
    content = normalized_text()

    assert (
        "Every Replay Result shall declare exactly one Replay Result Outcome."
        in content
    )

    for outcome in RESULT_OUTCOMES:
        assert outcome in content

    assert "Unsupported Replay Result Outcome shall fail validation." in content
    assert (
        "Replay Result Status and Replay Result Outcome shall remain "
        "independent normative concepts."
    ) in content


def test_equivalence_statuses_are_exact() -> None:
    content = normalized_text()

    assert "Replay Result shall declare exactly one Equivalence Status." in content

    for status in EQUIVALENCE_STATUSES:
        assert status in content

    assert "Missing Equivalence Status shall fail validation." in content


def test_divergence_statuses_are_exact() -> None:
    content = normalized_text()

    assert "Replay Result shall declare exactly one Divergence Status." in content

    for status in DIVERGENCE_STATUSES:
        assert status in content

    assert "Missing Divergence Status shall fail validation." in content


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


def test_reconstruction_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one immutable "
        "Replay Reconstruction.",
        "Replay Reconstruction Reference shall remain resolvable.",
        "Replay Reconstruction Reference shall remain immutable.",
        "Missing Replay Reconstruction Reference shall fail validation.",
    ):
        assert requirement in content


def test_comparison_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one immutable "
        "Replay Comparison.",
        "Replay Comparison Reference shall remain resolvable.",
        "Replay Comparison Reference shall remain immutable.",
        "Missing Replay Comparison Reference shall fail validation.",
    ):
        assert requirement in content


def test_validation_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one Replay Validation.",
        "Replay Validation Reference shall remain immutable.",
        "Replay Validation Reference shall remain resolvable.",
        "Missing Replay Validation Reference shall fail validation.",
    ):
        assert requirement in content


def test_divergence_reference_is_conditional() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one Replay Divergence "
        "when Outcome is DIVERGENT.",
        "Replay Divergence Reference shall remain immutable.",
        "Unresolved Replay Divergence Reference shall fail validation "
        "when required.",
    ):
        assert requirement in content


def test_completed_result_references_are_conditional() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one Replay Certification "
        "when Status is COMPLETED.",
        "Replay Result shall reference exactly one Replay Evidence "
        "when Status is COMPLETED.",
        "Replay Result shall reference exactly one Replay Attestation "
        "when Status is COMPLETED.",
    ):
        assert requirement in content


def test_failed_result_requires_failure_reference() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one Replay Failure "
        "when Status is FAILED.",
        "Replay Failure Reference shall remain immutable.",
        "Replay Failure Reference shall remain resolvable.",
        "Missing required Replay Failure Reference shall fail validation.",
    ):
        assert requirement in content


def test_result_evidence_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall reference exactly one Result Evidence.",
        "Result Evidence shall preserve all normative evidence "
        "supporting the Replay Result.",
        "Result Evidence shall remain immutable.",
        "Result Evidence shall remain completely traceable.",
        "Missing Result Evidence shall fail validation.",
        "Unresolved Result Evidence shall fail validation.",
    ):
        assert requirement in content


def test_result_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Result shall possess exactly one deterministic "
        "Result Integrity Reference."
    ) in content

    for binding in (
        "Replay Result Identity.",
        "Replay Result Version.",
        "Replay Result Status.",
        "Replay Result Outcome.",
        "Equivalence Status.",
        "Divergence Status.",
        "Result Evidence.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Result Integrity." in content
    assert "Result Integrity shall remain immutable." in content


def test_result_traceability_is_complete() -> None:
    content = normalized_text()

    for target in (
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Validation.",
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Attestation.",
        "Replay Failure.",
        "Result Evidence.",
        "Replay Integrity.",
        "Replay Traceability.",
    ):
        assert target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_result_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Result belongs to exactly one Replay.",
        "Replay Result references exactly one Replay Reconstruction.",
        "Replay Result references exactly one Replay Comparison.",
        "Replay Result references exactly one Replay Validation.",
        "Replay Result may reference one Replay Certification.",
        "Replay Result may reference one Replay Evidence.",
        "Replay Result may reference one Replay Attestation.",
        "Replay Result may reference one Replay Failure.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_result_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Result Ordering.",
        "Equivalent Replay Results shall produce identical ordering.",
        "Implementation-defined ordering is prohibited.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_result_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result shall preserve all mandatory Result information.",
        "Replay Result shall preserve all mandatory references.",
        "Replay Result shall preserve all mandatory traceability.",
        "Partial Replay Result shall fail validation.",
        "Missing mandatory Result information shall fail validation.",
    ):
        assert requirement in content


def test_result_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Validation.",
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Attestation.",
        "Replay Failure.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Result Evidence.",
        "Replay Result Status.",
        "Replay Result Outcome.",
        "Equivalence Status.",
        "Divergence Status.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Result shall never reinterpret preserved Replay artifacts.",
        "Replay Result shall never normalize preserved information.",
        "Replay Result shall never repair preserved information.",
        "Replay Result shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Result shall possess exactly one canonical serialization."
        in content
    )

    for preserved_property in (
        "Replay Result Identity.",
        "Replay Result Version.",
        "Replay Result Status.",
        "Replay Result Outcome.",
        "Equivalence Status.",
        "Divergence Status.",
        "Result Evidence.",
        "Result Integrity.",
        "Result Traceability.",
        "Replay Reconstruction Reference.",
        "Replay Comparison Reference.",
        "Replay Validation Reference.",
        "Replay Certification Reference.",
        "Replay Evidence Reference.",
        "Replay Attestation Reference.",
        "Replay Failure Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Result Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Result Ordering.",
        "Equivalent Replay Results shall produce identical ordering.",
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

    assert "Replay Result shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Result shall never modify, reinterpret, normalize, "
        "repair, replace, merge, or suppress historical artifacts."
    ) in content

    assert (
        "Replay Result shall preserve the original historical "
        "information exactly as recorded."
    ) in content


def test_replay_result_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Result shall remain immutable throughout "
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
        "Replay Result Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.20" in content
    assert "Replay Archive Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
