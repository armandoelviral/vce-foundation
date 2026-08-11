from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]

CONSTITUTION = ROOT / "docs" / "CONSTITUTION.md"
FREEZE = ROOT / "docs" / "RC001_CONSTITUTION_FREEZE.md"

EXPECTED_RCI = [f"{i:03d}" for i in range(1, 23)]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split())


def constitution_text() -> str:
    return read(CONSTITUTION)


def freeze_text() -> str:
    return read(FREEZE)


def rci_identifiers(text: str) -> list[str]:
    return re.findall(
        r"^RCI-(\d{3})$",
        text,
        flags=re.MULTILINE,
    )


# ---------------------------------------------------------------------
# Artifact existence
# ---------------------------------------------------------------------


def test_constitution_exists() -> None:
    assert CONSTITUTION.is_file()


def test_constitution_freeze_exists() -> None:
    assert FREEZE.is_file()


# ---------------------------------------------------------------------
# RC-001 identity
# ---------------------------------------------------------------------


def test_constitution_declares_rc001_identity() -> None:
    content = normalized(constitution_text())

    assert "Identifier RC-001" in content
    assert "Version 1.0" in content
    assert "Status Normative" in content
    assert "Model Constitutional Baseline" in content


def test_constitution_declares_promoted_authority() -> None:
    content = normalized(constitution_text())

    assert "Version 1.0" in content
    assert "Status Normative" in content
    assert "Model Constitutional Baseline" in content
    assert "Authority AUTHORITATIVE." in content
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


# ---------------------------------------------------------------------
# Canonical constitutional structure
# ---------------------------------------------------------------------


def test_constitution_declares_authority_context() -> None:
    content = constitution_text()

    assert "## Repository Authority Context" in content


def test_constitution_declares_highest_normative_authority() -> None:
    content = constitution_text()

    assert "## Highest Normative Authority" in content


def test_constitution_requires_unambiguous_current_authority() -> None:
    content = constitution_text()

    assert "## Unambiguous Current Authority" in content


def test_constitution_declares_principle_authority() -> None:
    content = constitution_text()

    assert "## Constitutional Principle Authority" in content


def test_constitution_declares_minimality() -> None:
    content = normalized(constitution_text())

    assert "Constitutional Minimality" in content
    assert "shall remain minimal" in content


def test_constitution_declares_conflict_resolution() -> None:
    content = constitution_text()

    assert "## Conflict Resolution" in content


def test_constitution_declares_versioned_authority() -> None:
    content = constitution_text()

    assert "## Versioned Constitutional Authority" in content


def test_constitution_declares_evolution() -> None:
    content = constitution_text()

    assert "## Constitutional Evolution" in content


def test_constitution_declares_evidence_driven_revision() -> None:
    content = normalized(constitution_text())

    assert "Evidence-Driven Revision" in content
    assert "Evidence shall have authority over attachment." in content


def test_constitution_declares_historical_traceability() -> None:
    content = constitution_text()

    assert "## Historical Traceability" in content


# ---------------------------------------------------------------------
# Authority model
# ---------------------------------------------------------------------


def test_authority_metadata_is_explicit() -> None:
    content = normalized(constitution_text())

    assert "Authority Metadata" in content
    assert "shall remain explicit and traceable" in content


def test_authority_metadata_is_implementation_independent() -> None:
    content = normalized(constitution_text())

    assert "Authority Metadata shall remain implementation-independent." in content


def test_bootstrap_authority_is_explicit() -> None:
    content = constitution_text()

    assert "## Bootstrap Authority" in content


def test_bootstrap_authority_is_single_use_per_lineage() -> None:
    content = normalized(constitution_text())

    assert (
        "Bootstrap Authority shall occur at most once "
        "per constitutional authority lineage."
        in content
    )


def test_bootstrap_authority_cannot_bypass_existing_authority() -> None:
    content = normalized(constitution_text())

    assert "Bootstrap Authority shall not be reused" in content
    assert "existing constitutional authority" in content


def test_authority_context_transition_is_explicit() -> None:
    content = normalized(constitution_text())

    assert "Repository Authority Context" in content
    assert "explicit and traceable" in content


# ---------------------------------------------------------------------
# Independence boundaries
# ---------------------------------------------------------------------


def test_implementation_independence_is_declared() -> None:
    content = constitution_text()

    assert "## Implementation Independence" in content


def test_technology_independence_is_declared() -> None:
    content = constitution_text()

    assert "## Technology Independence" in content


def test_constitution_is_not_bound_to_current_technologies() -> None:
    content = normalized(constitution_text())

    for technology in (
        "Python",
        "Rust",
        "OpenCV",
        "CUDA",
        "ONNX",
        "WASM",
        "Docker",
        "OCI",
    ):
        assert technology in content


def test_domain_semantics_remain_outside_constitution() -> None:
    content = normalized(constitution_text())

    assert "Domain Boundary" in content
    assert "shall not define domain-specific semantics" in content


def test_architecture_is_not_automatically_constitutional() -> None:
    content = normalized(constitution_text())

    assert "Architecture Boundary" in content
    assert (
        "shall not contain current architecture "
        "merely because that architecture is important."
        in content
    )


def test_emergency_operation_does_not_change_authority() -> None:
    content = normalized(constitution_text())

    assert "Emergency Boundary" in content
    assert "shall not silently modify constitutional authority" in content


# ---------------------------------------------------------------------
# Constitutional invariants
# ---------------------------------------------------------------------


def test_constitution_declares_exactly_twenty_two_invariants() -> None:
    identifiers = rci_identifiers(constitution_text())

    assert identifiers == EXPECTED_RCI


def test_constitution_has_no_duplicate_invariant_identifiers() -> None:
    identifiers = rci_identifiers(constitution_text())

    assert len(identifiers) == len(set(identifiers))


def test_rc001_invariants_are_sequential() -> None:
    assert rci_identifiers(constitution_text()) == EXPECTED_RCI


# ---------------------------------------------------------------------
# Freeze identity and scope
# ---------------------------------------------------------------------


def test_freeze_targets_rc001_v04() -> None:
    content = normalized(freeze_text())

    assert "Identifier RC-001-FREEZE" in content
    assert "Target RC-001 Version 0.4" in content


def test_freeze_does_not_self_promote() -> None:
    content = normalized(freeze_text())

    assert "does not itself grant authority" in content
    assert "RC-001 remains a Freeze Candidate" in content


def test_freeze_preserves_authority_context() -> None:
    content = freeze_text()

    assert "## Frozen Authority Context" in content


def test_freeze_preserves_current_authority_semantics() -> None:
    content = freeze_text()

    assert "## Frozen Current Authority Semantics" in content


def test_freeze_preserves_authority_metadata() -> None:
    content = freeze_text()

    assert "## Frozen Authority Metadata Principle" in content


def test_freeze_preserves_bootstrap_boundary() -> None:
    content = freeze_text()

    assert "## Frozen Bootstrap Authority" in content


def test_freeze_preserves_constitutional_invariants() -> None:
    content = normalized(freeze_text())

    assert "Frozen Constitutional Invariants" in content
    assert "RCI-001 through RCI-022" in content


# ---------------------------------------------------------------------
# Freeze mutation boundary
# ---------------------------------------------------------------------


def test_freeze_declares_explicitly_non_frozen_concerns() -> None:
    content = freeze_text()

    assert "## Explicitly Not Frozen" in content


def test_freeze_declares_permitted_changes() -> None:
    content = normalized(freeze_text())

    assert "Permitted Changes" in content
    assert "Typographical correction." in content
    assert "Formatting correction." in content


def test_freeze_declares_prohibited_changes() -> None:
    content = normalized(freeze_text())

    assert "Prohibited Changes" in content
    assert "Removing Repository Authority Context." in content
    assert "Reusing Bootstrap Authority" in content


def test_freeze_requires_versioned_breaking_evolution() -> None:
    content = normalized(freeze_text())

    assert "Breaking Evolution" in content
    assert "A new Constitution version." in content


# ---------------------------------------------------------------------
# Conformance and release
# ---------------------------------------------------------------------


def test_freeze_defines_conformance() -> None:
    content = freeze_text()

    assert "## Conformance" in content


def test_freeze_defines_release_criteria() -> None:
    content = freeze_text()

    assert "## Release Criteria" in content


def test_release_requires_executable_contract() -> None:
    content = normalized(freeze_text())

    assert "The executable Foundation contract passes." in content


def test_release_requires_promotion_gate() -> None:
    content = normalized(freeze_text())

    assert "A Promotion Gate explicitly grants normative authority." in content


# ---------------------------------------------------------------------
# Boundary protection
# ---------------------------------------------------------------------


def test_freeze_does_not_constitutionalize_current_architecture() -> None:
    content = normalized(freeze_text())

    assert "Common Trust Architecture." in content
    assert "Runtime semantics." in content
    assert "Domain semantics." in content
    assert "remain outside RC-001 constitutional semantics" in content


def test_implementation_cannot_create_constitutional_authority() -> None:
    content = normalized(constitution_text())

    assert "Implementation shall not create constitutional authority." in content


# ---------------------------------------------------------------------
# Terminal markers
# ---------------------------------------------------------------------


def test_constitution_has_terminal_marker() -> None:
    content = constitution_text()

    assert content.rstrip().endswith("# End of Constitution")


def test_freeze_has_terminal_marker() -> None:
    content = freeze_text()

    assert content.rstrip().endswith("# End of Constitution Freeze")
