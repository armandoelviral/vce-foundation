"""
Executable Specification

CKP-006.10
Commerce Reasoning Runtime Specification Freeze
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SPEC = (
    ROOT
    / "research"
    / "commerce"
    / "reasoning_runtime"
    / "CKP006_SPECIFICATION_FREEZE.md"
)

RUNTIME_SPECIFICATION_DIRECTORY = (
    ROOT
    / "research"
    / "commerce"
    / "reasoning_runtime"
)

CONTRACT_DIRECTORY = (
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
    "## Runtime Baseline",
    "## Validation Baseline",
    "## Replay Compatibility Baseline",
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
        "CKP-006.1 Commerce Reasoning Runtime Charter.",
        "CKP006_COMMERCE_REASONING_RUNTIME_CHARTER.md",
    ),
    (
        "CKP-006.2 Runtime Structure Model.",
        "CKP006_RUNTIME_STRUCTURE_MODEL.md",
    ),
    (
        "CKP-006.3 Runtime Execution Request Model.",
        "CKP006_RUNTIME_EXECUTION_REQUEST_MODEL.md",
    ),
    (
        "CKP-006.4 Runtime Execution Context Model.",
        "CKP006_RUNTIME_EXECUTION_CONTEXT_MODEL.md",
    ),
    (
        "CKP-006.5 Runtime State Model.",
        "CKP006_RUNTIME_STATE_MODEL.md",
    ),
    (
        "CKP-006.6 Runtime Transition Model.",
        "CKP006_RUNTIME_TRANSITION_MODEL.md",
    ),
    (
        "CKP-006.7 Runtime Stage Model.",
        "CKP006_RUNTIME_STAGE_MODEL.md",
    ),
    (
        "CKP-006.8 Runtime Artifact Registry Model.",
        "CKP006_RUNTIME_ARTIFACT_REGISTRY_MODEL.md",
    ),
    (
        "CKP-006.9 Runtime Result Model.",
        "CKP006_RUNTIME_RESULT_MODEL.md",
    ),
)

FROZEN_CONTRACTS = (
    "test_ckp006_commerce_reasoning_runtime_charter.py",
    "test_ckp006_runtime_structure_model.py",
    "test_ckp006_runtime_execution_request_model.py",
    "test_ckp006_runtime_execution_context_model.py",
    "test_ckp006_runtime_state_model.py",
    "test_ckp006_runtime_transition_model.py",
    "test_ckp006_runtime_stage_model.py",
    "test_ckp006_runtime_artifact_registry_model.py",
    "test_ckp006_runtime_result_model.py",
)

NORMATIVE_DEPENDENCIES = (
    "HAS Foundation 1.0 LTS.",
    "Specification Runtime 1.0.",
    "CKP-005 Baseline 1.0.",
    "CKP-005 Specification Freeze.",
    "CKP-006 Baseline 1.0.",
)

NORMATIVE_INTEGRITY_PROPERTIES = (
    "Canonical section ordering.",
    "Deterministic semantics.",
    "Fail-closed validation.",
    "Read-only boundaries.",
    "Normative terminology.",
    "Cross-document consistency.",
)

ALLOWED_EVOLUTION_RULES = (
    "Add new specifications.",
    "Add new baselines.",
    "Add new executable contracts.",
    "Extend compatible functionality.",
    "Clarify non-normative guidance.",
)

PROHIBITED_CHANGES = (
    "Modification of frozen deliverables.",
    "Modification of frozen contracts.",
    "Removal of canonical sections.",
    "Semantic reinterpretation.",
    "Behavioral modification.",
    "Compatibility regression.",
    "Determinism regression.",
    "Integrity regression.",
    "Replay compatibility regression.",
)

RELEASE_CRITERIA = (
    "Frozen deliverables.",
    "Frozen executable contracts.",
    "Successful validation.",
    "Zero failing specification contracts.",
    "Deterministic compatibility.",
    "Replay compatibility.",
    "Integrity preservation.",
)

COMPLIANCE_REQUIREMENTS = (
    "Conform to every frozen specification.",
    "Pass every frozen executable contract.",
    "Preserve deterministic behavior.",
    "Preserve replay compatibility.",
    "Preserve integrity.",
    "Preserve traceability.",
)

SUCCESS_CRITERIA = (
    "Baseline Version equals 1.0.",
    "All frozen deliverables are preserved.",
    "All frozen contracts are preserved.",
    "Normative integrity is preserved.",
    "Compatibility is preserved.",
    "Validation succeeds.",
    "Replay compatibility is preserved.",
    "Release criteria are satisfied.",
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

    assert "# CKP-006" in content
    assert (
        "Title Commerce Reasoning Runtime Specification Freeze"
        in content
    )
    assert "Abbreviation CRRSF" in content
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


def test_no_unexpected_level_two_headings_exist() -> None:
    assert tuple(level_two_headings()) == EXPECTED_SECTIONS


def test_purpose_declares_normative_freeze() -> None:
    content = normalized_text()

    for requirement in (
        "Establish the normative freeze for the "
        "Commerce Reasoning Runtime Specification.",
        "Freeze the complete CKP-006 Baseline 1.0.",
        "Preserve normative consistency.",
        "Preserve structural integrity.",
        "Preserve deterministic behavior.",
        "Preserve replay compatibility.",
        "Preserve executable specification compatibility.",
        "This Freeze introduces no additional Runtime behavior.",
        "This Freeze does not redefine any Runtime model.",
    ):
        assert requirement in content


def test_freeze_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-006-FREEZE-1.0",
        "The Freeze Identifier shall be globally unique.",
        "The Freeze Identifier shall remain immutable.",
    ):
        assert requirement in content


def test_freeze_version_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Freeze Version 1.0",
        "The Freeze Version identifies the frozen baseline.",
        "Unsupported Freeze Versions shall fail validation.",
    ):
        assert requirement in content


def test_freeze_status_is_frozen() -> None:
    content = normalized_text()

    assert "Status Frozen." in content
    assert (
        "A Frozen specification shall be treated as immutable."
        in content
    )


def test_baseline_version_is_exact() -> None:
    content = normalized_text()

    assert "CKP-006 Baseline 1.0." in content
    assert (
        "No alternative baseline shall exist within this Freeze."
        in content
    )


def test_all_frozen_deliverables_are_declared_once() -> None:
    content = normalized_text()

    for declaration, _ in FROZEN_DELIVERABLES:
        assert content.count(declaration) == 1, declaration


def test_frozen_deliverable_count_is_exact() -> None:
    content = normalized_text()

    declared = [
        declaration
        for declaration, _ in FROZEN_DELIVERABLES
        if declaration in content
    ]

    assert len(declared) == 9


def test_all_frozen_deliverable_files_exist() -> None:
    missing = [
        filename
        for _, filename in FROZEN_DELIVERABLES
        if not (
            RUNTIME_SPECIFICATION_DIRECTORY / filename
        ).is_file()
    ]

    assert not missing, f"Missing frozen deliverables: {missing}"


def test_no_additional_deliverables_belong_to_baseline() -> None:
    content = normalized_text()

    assert (
        "No additional deliverables belong to the "
        "CKP-006 Baseline 1.0 Freeze."
    ) in content


def test_all_frozen_contracts_are_declared_once() -> None:
    content = normalized_text()

    for contract in FROZEN_CONTRACTS:
        assert content.count(contract) == 1, contract


def test_frozen_contract_count_is_exact() -> None:
    content = normalized_text()

    declared = [
        contract
        for contract in FROZEN_CONTRACTS
        if contract in content
    ]

    assert len(declared) == 9


def test_all_frozen_contract_files_exist() -> None:
    missing = [
        contract
        for contract in FROZEN_CONTRACTS
        if not (CONTRACT_DIRECTORY / contract).is_file()
    ]

    assert not missing, f"Missing frozen contracts: {missing}"


def test_frozen_contract_properties_are_declared() -> None:
    content = normalized_text()

    assert "Frozen Contracts shall remain executable." in content
    assert "Frozen Contracts shall remain deterministic." in content


def test_normative_dependencies_are_declared() -> None:
    content = normalized_text()

    for dependency in NORMATIVE_DEPENDENCIES:
        assert dependency in content

    assert "Dependencies shall remain immutable." in content
    assert "Dependencies shall not be reinterpreted." in content


def test_normative_integrity_is_declared() -> None:
    content = normalized_text()

    for property_name in NORMATIVE_INTEGRITY_PROPERTIES:
        assert property_name in content

    assert (
        "Normative integrity violations shall fail validation."
        in content
    )


def test_baseline_integrity_is_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "The CKP-006 Baseline shall remain immutable.",
        "Every frozen document shall preserve its "
        "approved Version 1.0 content.",
        "Baseline mutation is prohibited.",
    ):
        assert requirement in content


def test_compatibility_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "All frozen deliverables shall remain mutually compatible.",
        "Compatibility shall remain deterministic.",
        "Compatibility regression is prohibited.",
    ):
        assert requirement in content


def test_backward_compatibility_policy_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Future revisions shall preserve compatibility "
        "with CKP-006 Baseline 1.0.",
        "Backward incompatible modifications require "
        "a new baseline.",
    ):
        assert requirement in content


def test_forward_compatibility_policy_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Future specifications may extend CKP-006.",
        "Extensions shall not redefine frozen artifacts.",
        "Extensions shall preserve deterministic behavior.",
    ):
        assert requirement in content


def test_change_control_policy_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "All proposed changes shall undergo formal review.",
        "Approved changes shall create a new baseline.",
        "Frozen artifacts shall not be modified in place.",
    ):
        assert requirement in content


def test_allowed_evolution_rules_are_declared() -> None:
    content = normalized_text()

    for rule in ALLOWED_EVOLUTION_RULES:
        assert rule in content

    assert (
        "Allowed evolution shall preserve all frozen artifacts."
        in content
    )


def test_prohibited_changes_are_declared() -> None:
    content = normalized_text()

    for prohibition in PROHIBITED_CHANGES:
        assert prohibition in content


def test_immutable_sections_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "All sections contained within every frozen "
        "CKP-006 specification shall remain immutable.",
        "Canonical ordering shall remain immutable.",
        "Executable contracts shall remain immutable.",
    ):
        assert requirement in content


def test_runtime_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "The Runtime Baseline consists of the complete "
        "set of frozen CKP-006 deliverables.",
        "Runtime Baseline shall remain deterministic.",
        "Runtime Baseline shall remain replay compatible.",
    ):
        assert requirement in content


def test_validation_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Validation shall be performed exclusively "
        "against the frozen executable contracts.",
        "Validation Baseline shall remain immutable.",
        "Validation shall remain fail-closed.",
    ):
        assert requirement in content


def test_replay_compatibility_baseline_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay compatibility shall be preserved across "
        "the complete Runtime Baseline.",
        "Replay behavior shall remain deterministic.",
        "Replay incompatibility shall fail validation.",
    ):
        assert requirement in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in RELEASE_CRITERIA:
        assert criterion in content


def test_freeze_approval_is_declared() -> None:
    content = normalized_text()

    for approval in (
        "CKP-006 Baseline 1.0 approved.",
        "Runtime Baseline approved.",
        "Executable contracts approved.",
        "Validation Baseline approved.",
        "Replay Compatibility Baseline approved.",
    ):
        assert approval in content


def test_governance_is_declared() -> None:
    content = normalized_text()

    for property_name in (
        "Normative consistency.",
        "Deterministic evolution.",
        "Version discipline.",
        "Formal review.",
        "Immutable baselines.",
    ):
        assert property_name in content


def test_compliance_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in COMPLIANCE_REQUIREMENTS:
        assert requirement in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in SUCCESS_CRITERIA:
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for frozen_item in (
        "CKP-006 Baseline.",
        "Frozen Deliverables.",
        "Frozen Contracts.",
        "Normative Integrity.",
        "Compatibility Baseline.",
        "Validation Baseline.",
        "Replay Compatibility Baseline.",
        "Governance.",
        "Compliance Requirements.",
    ):
        assert frozen_item in content

    assert "This Freeze introduces no Runtime behavior." in content
    assert "Future revisions shall preserve this Freeze." in content


def test_next_specification_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007" in content
    assert "Commerce Reasoning Replay." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
