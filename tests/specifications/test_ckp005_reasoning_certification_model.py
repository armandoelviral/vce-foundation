"""
Executable Specification

CKP-005.10
Commerce Reasoning Certification Model
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_REASONING_CERTIFICATION_MODEL.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Certification Identity",
    "## Certification Version",
    "## Certification Lifecycle",
    "## Certification Authority",
    "## Certification Policy",
    "## Certification Scope",
    "## Certification Target",
    "## Certification Inputs",
    "## Certification Preconditions",
    "## Certification Decision",
    "## Certification Status",
    "## Certification Record",
    "## Certification Validity",
    "## Certification Revocation",
    "## Certification Traceability",
    "## Certification Integrity",
    "## Canonical Serialization",
    "## Failure Classifications",
    "## Failure Conditions",
    "## Read-Only Boundary",
    "## Certification Invariants",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

CERTIFICATION_LIFECYCLE_VALUES = (
    "Draft.",
    "Certified.",
    "Suspended.",
    "Revoked.",
    "Expired.",
    "Superseded.",
    "Archived.",
)

CERTIFICATION_TARGETS = (
    "Reasoning Execution.",
    "Proof.",
    "Reasoning Evidence.",
    "Explanation.",
    "Validation Result.",
    "Validation Report.",
)

CERTIFICATION_INPUTS = (
    "Validation Result.",
    "Validation Report.",
    "Reasoning Evidence.",
    "Proof.",
    "Explanation.",
    "Specification Baseline.",
    "Certification Policy.",
    "Certification Authority.",
    "Integrity References.",
)

CERTIFICATION_PRECONDITIONS = (
    "Successful Validation.",
    "Validation Result PASS.",
    "Integrity Verification.",
    "Deterministic Validation.",
    "Complete Traceability.",
    "Policy Compliance.",
    "No unresolved violations.",
)

CERTIFICATION_DECISIONS = (
    "CERTIFIED.",
    "NOT_CERTIFIED.",
    "REVOKED.",
    "EXPIRED.",
    "SUPERSEDED.",
)

FAILURE_CLASSIFICATIONS = (
    "CERTIFICATION_IDENTITY_VIOLATION.",
    "CERTIFICATION_VERSION_VIOLATION.",
    "AUTHORITY_VIOLATION.",
    "POLICY_VIOLATION.",
    "PRECONDITION_VIOLATION.",
    "TRACEABILITY_VIOLATION.",
    "INTEGRITY_VIOLATION.",
    "SERIALIZATION_VIOLATION.",
    "READ_ONLY_VIOLATION.",
)

CERTIFICATION_INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Certification Identity.",
    "Certification Version Preservation.",
    "Exactly One Certification Authority.",
    "Exactly One Certification Policy.",
    "Exactly One Certification Scope.",
    "Exactly One Certification Target.",
    "Deterministic Certification Decision.",
    "Complete Traceability.",
    "Integrity Preservation.",
    "Canonical Serialization.",
    "Fail-Closed Certification.",
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

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Certification Model" in content
    assert "Abbreviation CRCM" in content
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

    assert (
        "Define the canonical, deterministic, immutable, "
        "independently verifiable, auditable, traceable, "
        "governable, and normatively executable Certification "
        "Model for the Commerce Knowledge Platform."
    ) in content

    assert (
        "The Commerce Reasoning Certification Model defines "
        "how a successfully validated Reasoning Execution may "
        "receive formal certification under a normative policy."
    ) in content

    assert "Certification shall recognize normative compliance." in content

    assert (
        "Certification shall establish formal trust over "
        "previously validated reasoning."
    ) in content


def test_certification_does_not_execute_or_modify_reasoning() -> None:
    content = normalized_text()

    for boundary in (
        "Certification shall not execute reasoning.",
        "Certification shall not perform validation.",
        "Certification shall not modify reasoning.",
        "Certification shall not modify proofs.",
        "Certification shall not modify evidence.",
        "Certification shall not modify explanations.",
    ):
        assert boundary in content


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in (
        "HAS Foundation 1.0 LTS.",
        "Specification Runtime 1.0.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
        "CKP-004 Commerce Query Language 1.0.",
        "CKP-005.1 Commerce Reasoning Charter.",
        "CKP-005.2 Commerce Reasoning Structure Model.",
        "CKP-005.3 Commerce Reasoning Request Model.",
        "CKP-005.4 Inference Rule Model.",
        "CKP-005.5 Fact and Premise Model.",
        "CKP-005.6 Proof Model.",
        "CKP-005.7 Reasoning Evidence Model.",
        "CKP-005.8 Explanation Model.",
        "CKP-005.9 Reasoning Validation Model.",
    ):
        assert dependency in content

    assert "Every dependency shall remain immutable." in content

    assert (
        "Certification shall never redefine or modify "
        "any dependency."
    ) in content


def test_certification_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall possess exactly one "
        "immutable Certification Identifier.",
        "CKP-CERTIFICATION-000001",
        "Certification Identity shall be globally unique.",
        "Certification Identity shall never be reused.",
        "Certification Identity shall remain independent "
        "from Certification Version.",
        "Missing, malformed, duplicated, or reused "
        "Certification Identity shall cause Certification failure.",
    ):
        assert requirement in content


def test_certification_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall declare exactly one "
        "Certification Version.",
        "The initial supported Certification Version is: 1.0.",
        "Certification Version identifies the normative "
        "Certification schema.",
        "Unsupported Certification Versions shall cause "
        "Certification failure.",
        "Certification Version shall not replace "
        "Certification Identity.",
    ):
        assert requirement in content


def test_certification_lifecycle_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall declare exactly one "
        "Lifecycle Status."
    ) in content

    for lifecycle in CERTIFICATION_LIFECYCLE_VALUES:
        assert lifecycle in content

    assert (
        "Lifecycle Status shall not regress except through "
        "explicitly defined revocation or supersession procedures."
    ) in content


def test_certification_authority_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall identify exactly one "
        "Certification Authority.",
        "Certification Authority shall remain immutable.",
        "Certification Authority shall be traceable.",
        "Unknown Certification Authorities shall be invalid.",
    ):
        assert requirement in content


def test_certification_policy_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall reference exactly one "
        "Certification Policy.",
        "Certification Policy shall define the normative "
        "admission criteria.",
        "Certification Policy shall remain immutable.",
        "Unsupported Certification Policies shall cause "
        "Certification failure.",
    ):
        assert requirement in content


def test_certification_scope_is_exactly_one_execution() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall certify exactly one "
        "Reasoning Execution.",
        "Certification Scope shall remain immutable.",
        "Certification Scope shall explicitly identify "
        "the validated Reasoning Request.",
    ):
        assert requirement in content


def test_certification_target_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall identify exactly one "
        "Certification Target."
    ) in content

    for target in CERTIFICATION_TARGETS:
        assert target in content

    assert "Unknown Certification Targets shall be invalid." in content


def test_certification_inputs_are_declared() -> None:
    content = normalized_text()

    for certification_input in CERTIFICATION_INPUTS:
        assert certification_input in content

    assert (
        "No undocumented input shall participate in Certification."
    ) in content


def test_certification_preconditions_are_declared() -> None:
    content = normalized_text()

    assert "Certification shall require:" in content

    for precondition in CERTIFICATION_PRECONDITIONS:
        assert precondition in content

    assert (
        "Failure of any prerequisite shall prohibit Certification."
    ) in content


def test_certification_requires_validation_pass() -> None:
    content = normalized_text()

    assert "Successful Validation." in content
    assert "Validation Result PASS." in content

    assert (
        "Certification shall not perform validation."
    ) in content


def test_certification_decision_is_exactly_one() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall produce exactly one "
        "Certification Decision."
    ) in content

    for decision in CERTIFICATION_DECISIONS:
        assert decision in content

    assert "Certification Decision shall remain immutable." in content


def test_certification_status_is_exactly_one() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall declare exactly one "
        "Certification Status.",
        "Certification Status shall reflect the current "
        "Certification lifecycle.",
        "Certification Status shall remain traceable.",
    ):
        assert requirement in content


def test_certification_record_is_exactly_one_and_immutable() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall produce exactly one "
        "Certification Record."
    ) in content

    for property_name in (
        "Certification Identity.",
        "Certification Version.",
        "Certification Authority.",
        "Certification Policy.",
        "Certification Target.",
        "Certification Decision.",
        "Certification Status.",
        "Validity Information.",
        "Integrity Reference.",
    ):
        assert property_name in content

    assert "Certification Record shall remain immutable." in content


def test_certification_validity_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Certification shall declare its Validity Period.",
        "Effective Date.",
        "Expiration Date.",
        "Validity shall be deterministic.",
        "Expired Certifications shall not be treated as "
        "active Certifications.",
    ):
        assert requirement in content


def test_certification_revocation_is_explicit_and_auditable() -> None:
    content = normalized_text()

    assert "Certification Revocation shall be explicit." in content

    for property_name in (
        "Revocation Reason.",
        "Revocation Timestamp.",
        "Revocation Authority.",
        "Revocation Integrity Reference.",
    ):
        assert property_name in content

    assert (
        "Revocation shall never erase historical "
        "Certification Records."
    ) in content


def test_certification_traceability_is_complete() -> None:
    content = normalized_text()

    assert "Every Certification shall be traceable to:" in content

    for artifact in (
        "Validation Result.",
        "Validation Report.",
        "Proof.",
        "Reasoning Evidence.",
        "Explanation.",
        "Certification Policy.",
        "Certification Authority.",
    ):
        assert artifact in content

    assert (
        "No Certification shall exist without complete traceability."
    ) in content


def test_certification_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall possess exactly one "
        "Certification Integrity Reference."
    ) in content

    for binding in (
        "Certification Identity.",
        "Certification Version.",
        "Certification Policy.",
        "Certification Authority.",
        "Certification Decision.",
        "Certification Record.",
        "Validation Result.",
        "Specification Baseline.",
    ):
        assert binding in content

    assert (
        "Any normative mutation shall invalidate "
        "Certification Integrity."
    ) in content


def test_canonical_serialization_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every Certification shall possess one deterministic "
        "canonical serialization."
    ) in content

    for preserved_property in (
        "Identity.",
        "Version.",
        "Authority.",
        "Policy.",
        "Decision.",
        "Status.",
        "Record.",
        "Integrity.",
    ):
        assert preserved_property in content

    assert "Presentation metadata shall be excluded." in content

    assert (
        "Canonical serialization shall be suitable for "
        "integrity calculation."
    ) in content


def test_failure_classifications_are_declared() -> None:
    content = normalized_text()

    for classification in FAILURE_CLASSIFICATIONS:
        assert classification in content


def test_failure_conditions_are_declared() -> None:
    content = normalized_text()

    for condition in (
        "Certification Identity is invalid.",
        "Certification Version is unsupported.",
        "Certification Authority is invalid.",
        "Certification Policy is unsupported.",
        "Validation Result is not PASS.",
        "Integrity cannot be established.",
        "Traceability cannot be established.",
        "Canonical serialization cannot be produced.",
        "Read-only boundaries are violated.",
    ):
        assert condition in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Execute reasoning.",
        "Execute validation.",
        "Modify reasoning.",
        "Modify proofs.",
        "Modify evidence.",
        "Modify explanations.",
        "Modify ontology.",
        "Modify graph.",
        "Modify immutable baselines.",
        "Repair invalid artifacts.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_certification_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in CERTIFICATION_INVARIANTS:
        assert invariant in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Identity is valid.",
        "Version is supported.",
        "Authority is valid.",
        "Policy is valid.",
        "Validation Result is PASS.",
        "Integrity is valid.",
        "Traceability is complete.",
        "Canonical serialization succeeds.",
        "No Failure Condition remains open.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    assert (
        "Version 1.0 defines the canonical Commerce "
        "Reasoning Certification Model."
    ) in content

    for excluded_capability in (
        "Cryptographic implementation.",
        "Digital signatures.",
        "Distributed governance.",
        "Consensus protocols.",
        "Blockchain integration.",
        "Interactive certification.",
        "Visualization.",
    ):
        assert excluded_capability in content

    assert (
        "Future implementations shall preserve this "
        "normative Certification contract."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005 Freeze." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
