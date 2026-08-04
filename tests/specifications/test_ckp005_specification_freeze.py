"""
Executable Specification

CKP-005
Commerce Reasoning Specification Freeze
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SPEC = (
    ROOT
    / "research"
    / "commerce"
    / "reasoning"
    / "CKP005_SPECIFICATION_FREEZE.md"
)

REASONING_DIRECTORY = (
    ROOT
    / "research"
    / "commerce"
    / "reasoning"
)

SPECIFICATION_DIRECTORY = (
    ROOT
    / "tests"
    / "specifications"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Freeze Identity",
    "## Freeze Version",
    "## Freeze Status",
    "## Baseline Version",
    "## Frozen Deliverables",
    "## Frozen Contracts",
    "## Normative Dependencies",
    "## Normative Integrity",
    "## Baseline Integrity",
    "## Compatibility Baseline",
    "## Backward Compatibility Policy",
    "## Forward Compatibility Policy",
    "## Change Control Policy",
    "## Allowed Evolution Rules",
    "## Prohibited Changes",
    "## Immutable Sections",
    "## Certification Baseline",
    "## Validation Baseline",
    "## Release Criteria",
    "## Freeze Approval",
    "## Governance",
    "## Compliance Requirements",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Specification",
)

FROZEN_DELIVERABLES = (
    (
        "CKP-005.1 Commerce Reasoning Charter.",
        "CKP005_COMMERCE_REASONING_CHARTER.md",
    ),
    (
        "CKP-005.2 Reasoning Structure Model.",
        "CKP005_REASONING_STRUCTURE_MODEL.md",
    ),
    (
        "CKP-005.3 Reasoning Request Model.",
        "CKP005_REASONING_REQUEST_MODEL.md",
    ),
    (
        "CKP-005.4 Inference Rule Model.",
        "CKP005_INFERENCE_RULE_MODEL.md",
    ),
    (
        "CKP-005.5 Fact and Premise Model.",
        "CKP005_FACT_AND_PREMISE_MODEL.md",
    ),
    (
        "CKP-005.6 Proof Model.",
        "CKP005_PROOF_MODEL.md",
    ),
    (
        "CKP-005.7 Reasoning Evidence Model.",
        "CKP005_REASONING_EVIDENCE_MODEL.md",
    ),
    (
        "CKP-005.8 Explanation Model.",
        "CKP005_EXPLANATION_MODEL.md",
    ),
    (
        "CKP-005.9 Reasoning Validation Model.",
        "CKP005_REASONING_VALIDATION_MODEL.md",
    ),
    (
        "CKP-005.10 Reasoning Certification Model.",
        "CKP005_REASONING_CERTIFICATION_MODEL.md",
    ),
)

FROZEN_CONTRACTS = (
    "test_ckp005_commerce_reasoning_charter.py",
    "test_ckp005_reasoning_structure_model.py",
    "test_ckp005_reasoning_request_model.py",
    "test_ckp005_inference_rule_model.py",
    "test_ckp005_fact_and_premise_model.py",
    "test_ckp005_proof_model.py",
    "test_ckp005_reasoning_evidence_model.py",
    "test_ckp005_explanation_model.py",
    "test_ckp005_reasoning_validation_model.py",
    "test_ckp005_reasoning_certification_model.py",
)

NORMATIVE_DEPENDENCIES = (
    "HAS Foundation 1.0 LTS.",
    "CKP-001.",
    "CKP-002.",
    "CKP-003.",
    "CKP-004.",
)

FREEZE_STATUS_VALUES = (
    "Draft.",
    "Approved.",
    "Frozen.",
    "Superseded.",
    "Archived.",
)

BASELINE_INTEGRITY_PROPERTIES = (
    "Identities.",
    "Versions.",
    "Dependencies.",
    "Contracts.",
    "Canonical ordering.",
    "Normative invariants.",
)

CHANGE_CONTROL_REQUIREMENTS = (
    "A new specification milestone.",
    "A normative document.",
    "An executable contract.",
    "Successful regression.",
    "Successful audit.",
    "Versioned approval.",
)

ALLOWED_EVOLUTION_RULES = (
    "Additive specifications.",
    "Independent modules.",
    "Major-version successors.",
    "Non-breaking extensions.",
)

PROHIBITED_CHANGES = (
    "Modification of frozen documents.",
    "Modification of frozen contracts.",
    "Removal of frozen sections.",
    "Semantic reinterpretation.",
    "Breaking compatibility.",
    "Silent normative changes.",
)

RELEASE_CRITERIA = (
    "All executable contracts passing.",
    "Regression passing.",
    "Audit passing.",
    "Clean repository.",
    "Approved Freeze.",
)

SUCCESS_CRITERIA = (
    "Every frozen document exists.",
    "Every executable contract passes.",
    "Every dependency is satisfied.",
    "Every invariant is preserved.",
    "The baseline is formally approved.",
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


def test_freeze_document_exists() -> None:
    assert SPEC.is_file()


def test_freeze_document_is_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_document_identity_is_declared() -> None:
    content = normalized_text()

    assert "# CKP-005" in content
    assert "Title Commerce Reasoning Specification Freeze" in content
    assert "Abbreviation CRSF" in content
    assert "Version 1.0" in content
    assert "Status Frozen" in content


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


def test_purpose_declares_official_freeze() -> None:
    content = normalized_text()

    for requirement in (
        "Define the official normative freeze of the "
        "Commerce Reasoning Specification.",
        "This document establishes the immutable "
        "Baseline 1.0 of CKP-005.",
        "The Freeze defines the normative boundary "
        "between completed specification work and all "
        "future evolution.",
        "The Freeze shall not introduce new reasoning behavior.",
        "The Freeze shall only establish the official baseline.",
    ):
        assert requirement in content


def test_freeze_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Specification Freeze shall possess "
        "exactly one immutable Freeze Identifier.",
        "CKP005-FREEZE-000001",
        "Freeze Identity shall be globally unique.",
        "Freeze Identity shall never be reused.",
    ):
        assert requirement in content


def test_freeze_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Every Freeze shall declare exactly one Freeze Version.",
        "The initial Freeze Version is: 1.0.",
        "Freeze Version identifies the frozen specification baseline.",
    ):
        assert requirement in content


def test_freeze_status_is_declared() -> None:
    content = normalized_text()

    for status in FREEZE_STATUS_VALUES:
        assert status in content

    assert "Version 1.0 is released with status: Frozen." in content


def test_baseline_version_is_declared() -> None:
    content = normalized_text()

    assert "CKP-005 Baseline 1.0." in content
    assert "All future revisions shall reference this baseline." in content


def test_all_frozen_deliverables_are_declared() -> None:
    content = normalized_text()

    for declaration, _ in FROZEN_DELIVERABLES:
        assert declaration in content


def test_all_frozen_deliverable_files_exist() -> None:
    missing = [
        filename
        for _, filename in FROZEN_DELIVERABLES
        if not (REASONING_DIRECTORY / filename).is_file()
    ]

    assert not missing, f"Missing frozen deliverables: {missing}"


def test_all_frozen_contracts_are_declared() -> None:
    content = normalized_text()

    for contract in FROZEN_CONTRACTS:
        assert contract in content


def test_all_frozen_contract_files_exist() -> None:
    missing = [
        contract
        for contract in FROZEN_CONTRACTS
        if not (SPECIFICATION_DIRECTORY / contract).is_file()
    ]

    assert not missing, f"Missing frozen contracts: {missing}"


def test_frozen_deliverable_count_is_exact() -> None:
    content = normalized_text()

    declared = [
        declaration
        for declaration, _ in FROZEN_DELIVERABLES
        if declaration in content
    ]

    assert len(declared) == 10


def test_frozen_contract_count_is_exact() -> None:
    content = normalized_text()

    declared = [
        contract
        for contract in FROZEN_CONTRACTS
        if contract in content
    ]

    assert len(declared) == 10


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in NORMATIVE_DEPENDENCIES:
        assert dependency in content

    assert (
        "Every dependency shall remain immutable for this baseline."
    ) in content


def test_normative_integrity_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Canonical semantics.",
        "Canonical ordering.",
        "Normative consistency.",
        "Complete traceability.",
        "Executable specifications.",
        "Cross-document integrity.",
    ):
        assert property_name in content

    assert (
        "No frozen document may contradict another frozen document."
    ) in content


def test_baseline_integrity_is_declared() -> None:
    content = normalized_text()

    for property_name in BASELINE_INTEGRITY_PROPERTIES:
        assert property_name in content

    assert "Integrity shall remain immutable." in content


def test_compatibility_baseline_is_declared() -> None:
    content = normalized_text()

    assert (
        "Baseline 1.0 defines the official compatibility "
        "reference for every future CKP-005 evolution."
    ) in content


def test_backward_compatibility_policy_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Modify frozen semantics.",
        "Break executable contracts.",
        "Remove frozen sections.",
        "Invalidate existing certification.",
    ):
        assert prohibition in content


def test_forward_compatibility_policy_is_declared() -> None:
    content = normalized_text()

    for permission in (
        "Add new capabilities.",
        "Add new specification modules.",
        "Publish new major versions.",
        "Extend existing functionality without modifying Baseline 1.0.",
    ):
        assert permission in content


def test_change_control_policy_is_declared() -> None:
    content = normalized_text()

    for requirement in CHANGE_CONTROL_REQUIREMENTS:
        assert requirement in content


def test_allowed_evolution_rules_are_declared() -> None:
    content = normalized_text()

    for rule in ALLOWED_EVOLUTION_RULES:
        assert rule in content


def test_prohibited_changes_are_declared() -> None:
    content = normalized_text()

    for prohibition in PROHIBITED_CHANGES:
        assert prohibition in content


def test_immutable_sections_are_declared() -> None:
    content = normalized_text()

    for immutable_item in (
        "All CKP-005.1 through CKP-005.10 documents.",
        "All executable contracts.",
        "Baseline Version.",
        "Freeze Identity.",
        "Normative ordering.",
    ):
        assert immutable_item in content


def test_certification_baseline_is_declared() -> None:
    content = normalized_text()

    assert (
        "Certification Baseline 1.0 is defined by the "
        "frozen CKP-005 specification."
    ) in content


def test_validation_baseline_is_declared() -> None:
    content = normalized_text()

    assert (
        "Validation Baseline 1.0 shall evaluate "
        "conformance exclusively against the frozen specification."
    ) in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in RELEASE_CRITERIA:
        assert criterion in content


def test_freeze_approval_is_declared() -> None:
    content = normalized_text()

    assert (
        "Baseline 1.0 is approved as the official "
        "Commerce Reasoning Specification Freeze."
    ) in content
    assert "Approval Status: Frozen." in content


def test_governance_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Future governance shall preserve this baseline.",
        "Every future specification shall explicitly reference "
        "this Freeze.",
    ):
        assert requirement in content


def test_compliance_requirements_are_declared() -> None:
    content = normalized_text()

    assert (
        "Every conforming implementation shall satisfy "
        "Baseline 1.0 without modification."
    ) in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in SUCCESS_CRITERIA:
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Baseline 1.0 establishes the official release "
        "boundary of CKP-005.",
        "Future revisions shall preserve this boundary.",
    ):
        assert requirement in content


def test_next_specification_is_declared() -> None:
    content = normalized_text()

    assert "CKP-006" in content
    assert "Commerce Reasoning Runtime." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
