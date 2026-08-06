"""
Executable Specification

CKP-007.17
Commerce Replay Attestation Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_REPLAY_ATTESTATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Replay Attestation Identity",
    "## Replay Attestation Version",
    "## Replay Attestation Lifecycle",
    "## Replay Attestation Scope",
    "## Replay Attestation Inputs",
    "## Replay Attestation Preconditions",
    "## Replay Certification Reference",
    "## Replay Evidence Reference",
    "## Attestation Identity",
    "## Attestation Subject",
    "## Attestation Claims",
    "## Attestation Basis",
    "## Attestation Authority",
    "## Attestation Validity",
    "## Attestation Integrity",
    "## Attestation Traceability",
    "## Attestation Relationships",
    "## Attestation Ordering",
    "## Attestation Completeness",
    "## Attestation Consistency",
    "## Canonical Serialization",
    "## Deterministic Ordering",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Historical Boundary",
    "## Replay Attestation Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Attesting.",
    "Completed.",
    "Archived.",
)

VALIDITY_STATES = (
    "Pending.",
    "Valid.",
    "Invalid.",
)

REQUIRED_INPUTS = (
    "Replay Attestation Identifier.",
    "Replay Attestation Version.",
    "Replay Certification Reference.",
    "Replay Evidence Reference.",
    "Replay Validation Reference.",
    "Replay Result Reference.",
    "Attestation Identifier.",
    "Attestation Subject.",
    "Attestation Claims.",
    "Attestation Basis.",
    "Attestation Authority.",
    "Attestation Validity.",
    "Attestation Integrity Reference.",
    "Attestation Traceability Reference.",
    "Replay Attestation Integrity Reference.",
)

PRECONDITIONS = (
    "Validated Replay Certification.",
    "Validated Replay Evidence.",
    "Validated Replay Validation.",
    "Resolved Replay Result.",
    "Verified Replay Integrity.",
    "Verified Replay Traceability.",
)

CENTRAL_RULES = (
    "Replay Attestation shall preserve exactly one Replay.",
    "Replay Attestation shall require exactly one Replay Certification.",
    "Replay Attestation shall require exactly one Replay Evidence.",
    "Replay Attestation shall preserve Replay Validation.",
    "Replay Attestation shall preserve Replay Integrity.",
    "Replay Attestation shall preserve Replay Traceability.",
    "Replay Attestation shall preserve Attestation Claims.",
    "Replay Attestation shall be deterministic.",
    "Replay Attestation shall remain immutable.",
    "Replay Attestation shall fail closed.",
)

FAILURE_CLASSIFICATIONS = (
    "REPLAY_ATTESTATION_IDENTITY_VIOLATION.",
    "REPLAY_ATTESTATION_VERSION_VIOLATION.",
    "REPLAY_ATTESTATION_LIFECYCLE_VIOLATION.",
    "REPLAY_ATTESTATION_SCOPE_VIOLATION.",
    "REPLAY_ATTESTATION_INPUT_VIOLATION.",
    "REPLAY_ATTESTATION_PRECONDITION_VIOLATION.",
    "REPLAY_ATTESTATION_REFERENCE_VIOLATION.",
    "ATTESTATION_IDENTITY_VIOLATION.",
    "ATTESTATION_SUBJECT_VIOLATION.",
    "ATTESTATION_CLAIMS_VIOLATION.",
    "ATTESTATION_BASIS_VIOLATION.",
    "ATTESTATION_AUTHORITY_VIOLATION.",
    "ATTESTATION_VALIDITY_VIOLATION.",
    "ATTESTATION_INTEGRITY_VIOLATION.",
    "ATTESTATION_TRACEABILITY_VIOLATION.",
    "ATTESTATION_RELATIONSHIP_VIOLATION.",
    "ATTESTATION_ORDERING_VIOLATION.",
    "ATTESTATION_COMPLETENESS_VIOLATION.",
    "ATTESTATION_CONSISTENCY_VIOLATION.",
    "REPLAY_ATTESTATION_SERIALIZATION_VIOLATION.",
    "REPLAY_ATTESTATION_FAILURE.",
    "READ_ONLY_VIOLATION.",
)

FAILURE_CONDITIONS = (
    "Replay Attestation Identity is invalid.",
    "Replay Attestation Version is unsupported.",
    "Mandatory inputs are missing.",
    "Mandatory references cannot be resolved.",
    "Replay Certification cannot be resolved.",
    "Replay Evidence cannot be resolved.",
    "Replay Validation cannot be resolved.",
    "Replay Result cannot be resolved.",
    "Attestation Integrity verification fails.",
    "Attestation Traceability verification fails.",
    "Attestation Claims are incomplete.",
    "Attestation Basis is incomplete.",
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
    "Historical References.",
    "Frozen Baselines.",
)

INVARIANTS = (
    "Exactly one Replay Attestation Identity.",
    "Exactly one Replay.",
    "Exactly one Replay Certification.",
    "Exactly one Replay Evidence.",
    "Exactly one Attestation Subject.",
    "Exactly one Replay Attestation Integrity Reference.",
    "Identity Preservation.",
    "Certification Preservation.",
    "Evidence Preservation.",
    "Attestation Preservation.",
    "Integrity Preservation.",
    "Traceability Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Attestation.",
)

SUCCESS_CRITERIA = (
    "Identity is valid.",
    "Version is supported.",
    "Lifecycle is valid.",
    "Scope is valid.",
    "Inputs are complete.",
    "Preconditions are satisfied.",
    "Replay Certification resolves successfully.",
    "Replay Evidence resolves successfully.",
    "Replay Validation resolves successfully.",
    "Replay Result resolves successfully.",
    "Attestation Claims are complete.",
    "Attestation Basis is complete.",
    "Attestation Validity is consistent.",
    "Attestation Integrity is verified.",
    "Attestation Traceability is complete.",
    "Canonical serialization succeeds.",
    "Deterministic ordering succeeds.",
    "All invariants are preserved.",
)

RELEASE_CAPABILITIES = (
    "Replay Attestation Identity.",
    "Replay Attestation Version.",
    "Replay Attestation Lifecycle.",
    "Replay Attestation Scope.",
    "Replay Attestation Inputs.",
    "Replay Attestation Preconditions.",
    "Replay Certification Reference.",
    "Replay Evidence Reference.",
    "Attestation Identity.",
    "Attestation Subject.",
    "Attestation Claims.",
    "Attestation Basis.",
    "Attestation Authority.",
    "Attestation Validity.",
    "Attestation Integrity.",
    "Attestation Traceability.",
    "Attestation Relationships.",
    "Attestation Ordering.",
    "Attestation Completeness.",
    "Attestation Consistency.",
    "Canonical Serialization.",
    "Deterministic Ordering.",
    "Failure Behavior.",
    "Read-Only Historical Boundary.",
    "Replay Attestation Invariants.",
)

RELEASE_EXCLUSIONS = (
    "Replay engine implementation.",
    "Attestation engine.",
    "PKI.",
    "Digital signatures.",
    "Cryptographic algorithms.",
    "Certificates.",
    "TPM.",
    "SGX.",
    "TDX.",
    "SEV.",
    "Persistence.",
    "WAL.",
    "Event sourcing.",
    "Scheduler.",
    "Concurrency.",
    "Distributed infrastructure.",
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
    assert "Title Commerce Replay Attestation Model" in content
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

    for lifecycle_state in LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "No additional lifecycle states shall be defined" in content
    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_validity_states_are_exact() -> None:
    content = normalized_text()

    for validity_state in VALIDITY_STATES:
        assert validity_state in content

    assert (
        "Lifecycle and Validity shall remain independent normative concepts."
        in content
    )


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
        "Replay Attestation shall reference exactly one immutable "
        "Replay Certification.",
        "Replay Certification Reference shall remain resolvable.",
        "Replay Certification Reference shall remain immutable.",
        "Replay Certification Reference shall preserve "
        "certification traceability.",
        "Missing Replay Certification Reference shall fail validation.",
        "Unresolved Replay Certification Reference shall fail validation.",
    ):
        assert requirement in content


def test_replay_evidence_reference_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Attestation shall reference exactly one immutable "
        "Replay Evidence.",
        "Replay Evidence Reference shall remain resolvable.",
        "Replay Evidence Reference shall remain immutable.",
        "Replay Evidence Reference shall preserve evidence traceability.",
        "Missing Replay Evidence Reference shall fail validation.",
        "Unresolved Replay Evidence Reference shall fail validation.",
    ):
        assert requirement in content


def test_attestation_identity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Attestation shall possess exactly one immutable "
        "Attestation Identifier.",
        "Attestation Identity shall be globally unique.",
        "Attestation Identity shall never be reused.",
        "Missing Attestation Identifier shall fail validation.",
        "Malformed Attestation Identifier shall fail validation.",
        "Duplicated Attestation Identifier shall fail validation.",
    ):
        assert requirement in content


def test_attestation_subject_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Attestation shall declare exactly one "
        "Attestation Subject.",
        "Attestation Subject identifies the Replay that is the "
        "subject of the Attestation.",
        "Attestation Subject shall remain immutable.",
        "Missing Attestation Subject shall fail validation.",
    ):
        assert requirement in content


def test_attestation_claims_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Attestation shall declare exactly one complete "
        "Attestation Claims set.",
        "Attestation Claims shall represent the normative statements "
        "supported by the Replay Certification and Replay Evidence.",
        "Attestation Claims shall remain immutable.",
        "Incomplete Attestation Claims shall fail validation.",
        "Unsupported Attestation Claims shall fail validation.",
    ):
        assert requirement in content


def test_attestation_basis_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Attestation shall declare exactly one Attestation Basis."
        in content
    )

    for reference in (
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Validation.",
        "Replay Result.",
    ):
        assert reference in content

    assert "Attestation Basis shall remain immutable." in content
    assert "Missing Attestation Basis shall fail validation." in content


def test_attestation_authority_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay Attestation shall declare exactly one "
        "Attestation Authority.",
        "Attestation Authority identifies the normative authority "
        "responsible for the Attestation.",
        "Attestation Authority shall remain immutable.",
        "Unknown Attestation Authority shall fail validation.",
        "This specification defines no cryptographic authority model.",
    ):
        assert requirement in content


def test_attestation_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Attestation shall possess exactly one deterministic "
        "Attestation Integrity Reference."
    ) in content

    for binding in (
        "Attestation Identity.",
        "Replay Attestation Identity.",
        "Replay Certification Reference.",
        "Replay Evidence Reference.",
        "Attestation Subject.",
        "Attestation Claims.",
        "Attestation Basis.",
        "Attestation Validity.",
    ):
        assert binding in content

    assert "Mutation shall invalidate Attestation Integrity." in content
    assert "Attestation Integrity shall remain immutable." in content


def test_attestation_traceability_is_complete() -> None:
    content = normalized_text()

    for traceability_target in (
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Validation.",
        "Replay Result.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Attestation Basis.",
    ):
        assert traceability_target in content

    assert "Traceability shall remain complete." in content
    assert "Broken traceability shall fail validation." in content


def test_attestation_relationships_are_declared() -> None:
    content = normalized_text()

    for relationship in (
        "Replay Attestation belongs to exactly one Replay.",
        "Replay Attestation references exactly one Replay Certification.",
        "Replay Attestation references exactly one Replay Evidence.",
        "Replay Attestation references exactly one Replay Validation.",
        "Replay Attestation references exactly one Replay Result.",
        "Relationships shall remain explicit.",
        "Relationships shall remain immutable.",
        "Relationships shall preserve complete traceability.",
    ):
        assert relationship in content


def test_attestation_ordering_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Attestation Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Attestation Ordering.",
        "Implementation-defined ordering is prohibited.",
        "Attestation Ordering shall remain immutable.",
        "Ordering violations shall fail validation.",
    ):
        assert requirement in content


def test_attestation_completeness_is_required() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Attestation shall preserve all mandatory "
        "Attestation information.",
        "Replay Attestation shall preserve all mandatory references.",
        "Replay Attestation shall preserve all mandatory traceability.",
        "Partial Replay Attestation shall fail validation.",
        "Missing mandatory Attestation information shall fail validation.",
    ):
        assert requirement in content


def test_attestation_consistency_is_declared() -> None:
    content = normalized_text()

    for target in (
        "Replay Certification.",
        "Replay Evidence.",
        "Replay Validation.",
        "Replay Result.",
        "Replay Integrity.",
        "Replay Traceability.",
        "Attestation Basis.",
        "Attestation Claims.",
    ):
        assert target in content

    for requirement in (
        "Consistency violations shall fail validation.",
        "Replay Attestation shall never reinterpret preserved "
        "Replay artifacts.",
        "Replay Attestation shall never normalize preserved information.",
        "Replay Attestation shall never repair preserved information.",
        "Replay Attestation shall remain deterministic throughout "
        "its entire lifecycle.",
    ):
        assert requirement in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Replay Attestation shall possess exactly one "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Replay Attestation Identity.",
        "Replay Attestation Version.",
        "Attestation Identity.",
        "Attestation Subject.",
        "Attestation Claims.",
        "Attestation Basis.",
        "Attestation Authority.",
        "Attestation Validity.",
        "Attestation Integrity.",
        "Attestation Traceability.",
        "Replay Certification Reference.",
        "Replay Evidence Reference.",
    ):
        assert preserved_property in content

    assert "Canonical serialization shall remain deterministic." in content
    assert "Canonical serialization shall remain immutable." in content
    assert "Serialization failures shall fail validation." in content


def test_deterministic_ordering_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay Attestation Ordering shall be deterministic.",
        "Equivalent Replay inputs shall produce equivalent "
        "Replay Attestation Ordering.",
        "Equivalent Replay Attestations shall produce identical ordering.",
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

    assert "Replay Attestation shall never modify:" in content

    for target in READ_ONLY_TARGETS:
        assert target in content

    assert (
        "Replay Attestation shall never modify, reinterpret, normalize, "
        "repair, replace, merge, or suppress historical artifacts."
    ) in content

    assert (
        "Replay Attestation shall preserve the original historical "
        "information exactly as certified."
    ) in content


def test_replay_attestation_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content

    assert (
        "Replay Attestation shall remain immutable throughout "
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
        "Replay Attestation Model."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.18" in content
    assert "Replay Failure Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
