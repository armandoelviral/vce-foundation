"""
Executable Specification

CKP-007.16
Commerce Replay Evidence Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_EVIDENCE_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Evidence Identity",
    "## Replay Evidence Version",
    "## Replay Evidence Lifecycle",
    "## Replay Evidence Scope",
    "## Replay Evidence Inputs",
    "## Replay Evidence Preconditions",
    "## Replay Certification Reference",
    "## Evidence Identity",
    "## Evidence Classification",
    "## Evidence Source",
    "## Evidence Provenance",
    "## Evidence Composition",
    "## Evidence Integrity",
    "## Evidence Traceability",
    "## Evidence Relationships",
    "## Evidence Ordering",
    "## Evidence Completeness",
    "## Evidence Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Evidence Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Collecting.",
    "Completed.",
    "Archived.",
)

REQUIRED_INPUTS = (
    "Replay Evidence Identifier.",
    "Replay Evidence Version.",
    "Replay Certification Reference.",
    "Replay Validation Reference.",
    "Replay Reconstruction Reference.",
    "Replay Comparison Reference.",
    "Replay Divergence Reference.",
    "Replay Result Reference.",
    "Evidence Identifier.",
    "Evidence Classification.",
    "Evidence Source.",
    "Evidence Provenance.",
    "Evidence Composition.",
    "Evidence Integrity Reference.",
    "Evidence Traceability Reference.",
    "Replay Evidence Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Certification.",
    "Validated Replay Validation.",
    "Validated Replay Reconstruction.",
    "Validated Replay Comparison.",
    "Validated Replay Divergence.",
    "Resolved Replay Result.",
    "Verified Replay Integrity.",
    "Verified Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Evidence shall preserve exactly one Replay.",
    "Replay Evidence shall require exactly one Replay Certification.",
    "Replay Evidence shall preserve Replay Validation.",
    "Replay Evidence shall preserve Replay Reconstruction.",
    "Replay Evidence shall preserve Replay Comparison.",
    "Replay Evidence shall preserve Replay Divergence.",
    "Replay Evidence shall preserve Replay Integrity.",
    "Replay Evidence shall preserve Replay Traceability.",
    "Replay Evidence shall be deterministic.",
    "Replay Evidence shall remain immutable.",
    "Replay Evidence shall fail closed.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_EVIDENCE_IDENTITY_VIOLATION.",
    "REPLAY_EVIDENCE_VERSION_VIOLATION.",
    "REPLAY_EVIDENCE_LIFECYCLE_VIOLATION.",
    "REPLAY_EVIDENCE_SCOPE_VIOLATION.",
    "REPLAY_EVIDENCE_INPUT_VIOLATION.",
    "REPLAY_EVIDENCE_PRECONDITION_VIOLATION.",
    "REPLAY_EVIDENCE_REFERENCE_VIOLATION.",
    "EVIDENCE_IDENTITY_VIOLATION.",
    "EVIDENCE_CLASSIFICATION_VIOLATION.",
    "EVIDENCE_SOURCE_VIOLATION.",
    "EVIDENCE_PROVENANCE_VIOLATION.",
    "EVIDENCE_COMPOSITION_VIOLATION.",
    "EVIDENCE_INTEGRITY_VIOLATION.",
    "EVIDENCE_TRACEABILITY_VIOLATION.",
    "EVIDENCE_RELATIONSHIP_VIOLATION.",
    "EVIDENCE_ORDERING_VIOLATION.",
    "EVIDENCE_COMPLETENESS_VIOLATION.",
    "EVIDENCE_CONSISTENCY_VIOLATION.",
    "REPLAY_EVIDENCE_SERIALIZATION_VIOLATION.",
    "REPLAY_EVIDENCE_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Evidence Identity is invalid.",
    "Replay Evidence Version is unsupported.",
    "Mandatory inputs are missing.",
    "Mandatory references cannot be resolved.",
    "Replay Certification cannot be resolved.",
    "Replay Validation cannot be resolved.",
    "Replay Reconstruction cannot be resolved.",
    "Replay Comparison cannot be resolved.",
    "Replay Divergence cannot be resolved.",
    "Replay Result cannot be resolved.",
    "Evidence Integrity verification fails.",
    "Evidence Traceability verification fails.",
    "Evidence Provenance is incomplete.",
    "Evidence Composition is incomplete.",
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
    "Historical Replay Evidence.",
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Evidence Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Certification.",
    "Exactly one Evidence Composition.",
    "Exactly one Replay Evidence Integrity Reference.",
    "Identity Preservation.",
    "Certification Preservation.",
    "Evidence Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Evidence.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Certification resolves successfully.",
    "Replay Validation resolves successfully.",
    "Replay Reconstruction resolves successfully.",
    "Replay Comparison resolves successfully.",
    "Replay Divergence resolves successfully.",
    "Replay Result resolves successfully.",
    "Evidence Composition is complete.",
    "Evidence Provenance is complete.",
    "Evidence Integrity is verified.",
    "Evidence Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Evidence Identity.",
    "Replay Evidence Version.",
    "Replay Evidence Lifecycle.",
    "Replay Evidence Scope.",
    "Replay Evidence Inputs.",
    "Replay Evidence Preconditions.",
    "Replay Certification Reference.",
    "Evidence Identity.",
    "Evidence Classification.",
    "Evidence Source.",
    "Evidence Provenance.",
    "Evidence Composition.",
    "Evidence Integrity.",
    "Evidence Traceability.",
    "Evidence Relationships.",
    "Evidence Ordering.",
    "Evidence Completeness.",
    "Evidence Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Evidence Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Replay engine implementation.",
    "Evidence collector.",
    "Evidence capture mechanisms.",
    "Storage formats.",
    "Persistence.",
    "WAL.",
    "Event sourcing.",
    "Transport.",
    "Schedulers.",
    "Concurrency.",
    "Distributed infrastructure.",
    "Cryptographic algorithms.",
    "PKI.",
    "Digital signatures.",
    "HSM.",
    "Object storage.",
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
    assert "Title Commerce Replay Evidence Model" in content
    assert "Abbreviation CREM" in content
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


def test_replay_certification_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Evidence shall reference exactly one immutable "
        "Replay Certification.",
        "Replay Certification Reference shall remain resolvable.",
        "Replay Certification Reference shall remain immutable.",
        "Missing Replay Certification Reference shall fail validation.",
        "Unresolved Replay Certification Reference shall fail validation.",
    ):
        assert requirement in content


def test_evidence_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Evidence shall possess exactly one immutable "
        "Evidence Identifier.",
        "Evidence Identity shall be globally unique.",
        "Evidence Identity shall never be reused.",
        "Missing Evidence Identifier shall fail validation.",
        "Malformed Evidence Identifier shall fail validation.",
        "Duplicated Evidence Identifier shall fail validation.",
    ):
        assert requirement in content


def test_evidence_classification_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Evidence shall declare exactly one Evidence Classification.",
        "Evidence Classification shall identify the normative role "
        "of the Evidence.",
        "Evidence Classification shall remain immutable.",
        "Unsupported Evidence Classification shall fail validation.",
    ):
        assert requirement in content


def test_evidence_source_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Evidence shall declare exactly one Evidence Source.",
        "Evidence Source identifies the normative origin of the Evidence.",
        "Evidence Source shall remain immutable.",
        "Unknown Evidence Source shall fail validation.",
    ):
        assert requirement in content


def test_evidence_provenance_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Evidence shall preserve exactly one Evidence Provenance.",
        "Evidence Provenance shall remain immutable.",
        "Evidence Provenance shall remain complete.",
        "Incomplete Evidence Provenance shall fail validation.",
    ):
        assert requirement in content


def test_evidence_composition_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Evidence shall preserve exactly one Evidence Composition.",
        "Evidence Composition shall contain the complete normative "
        "Evidence Set associated with exactly one Replay.",
        "Evidence Composition shall remain immutable.",
        "Evidence Composition shall remain deterministic.",
        "Partial Evidence Composition shall fail validation.",
    ):
        assert requirement in content


def test_evidence_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Evidence shall possess exactly one deterministic "
        "Evidence Integrity Reference."
    ) in content

    for binding in (
        "Evidence Identity.",
        "Replay Evidence Identity.",
        "Replay Certification Reference.",
        "Evidence Composition.",
        "Evidence Provenance.",
        "Evidence Traceability.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Evidence Integrity." in content
    assert "Evidence Integrity shall remain immutable." in content


def test_evidence_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Replay Certification.",
        "Replay Validation.",
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Divergence.",
        "Replay Result.",
        "Replay Integrity.",
        "Evidence Provenance.",
    ):
        assert traceability_target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_evidence_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Evidence belongs to exactly one Replay.",
        "Replay Evidence references exactly one Replay Certification.",
        "Replay Evidence references exactly one Replay Validation.",
        "Replay Evidence references exactly one Replay Reconstruction.",
        "Replay Evidence references exactly one Replay Comparison.",
        "Replay Evidence references exactly one Replay Divergence.",
        "Replay Evidence references exactly one Replay Result.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_evidence_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Evidence Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Evidence Ordering.",
        "Implementation-defined ordering is prohibited.",
        "Evidence Ordering shall remain immutable.",
    ):
        assert requirement in content


def test_evidence_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Evidence shall preserve all mandatory Evidence.",
        "Replay Evidence shall preserve all mandatory references.",
        "Replay Evidence shall preserve all mandatory traceability.",
        "Partial Replay Evidence shall fail validation.",
        "Missing mandatory Evidence shall fail validation.",
    ):
        assert requirement in content


def test_evidence_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Certification.",
        "Replay Validation.",
        "Replay Reconstruction.",
        "Replay Comparison.",
        "Replay Divergence.",
        "Replay Result.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Evidence Provenance.",
        "Evidence Composition.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Evidence shall never reinterpret preserved Evidence.",
        "Replay Evidence shall never normalize preserved Evidence.",
        "Replay Evidence shall never repair preserved Evidence.",
        "Replay Evidence shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Evidence shall possess exactly one canonical serialization."
        in content
    )

    for preserved_property in (
        "Replay Evidence Identity.",
        "Replay Evidence Version.",
        "Evidence Identity.",
        "Evidence Classification.",
        "Evidence Source.",
        "Evidence Provenance.",
        "Evidence Composition.",
        "Evidence Integrity.",
        "Evidence Traceability.",
        "Replay Certification Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Evidence Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Evidence Ordering.",
        "Equivalent Replay Evidence shall produce identical ordering.",
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

    assert "Replay Evidence shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Evidence shall never modify, reinterpret, normalize, "
        "repair, replace, merge, or suppress historical Evidence."
    ) in content
    assert (
        "Replay Evidence shall preserve the original historical "
        "Evidence exactly as certified."
    ) in content


def test_replay_evidence_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Evidence shall remain immutable throughout "
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
        "Replay Evidence Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.17" in content
    assert "Replay Attestation Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
