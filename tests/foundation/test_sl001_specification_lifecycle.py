from pathlib import Path
import re


SPEC = Path("architecture/SPECIFICATION_LIFECYCLE.md")
FREEZE = Path("architecture/SL001_SPECIFICATION_FREEZE.md")

REFUTATION_DIR = Path(
    "research/foundation/specification_lifecycle"
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def freeze_text() -> str:
    return FREEZE.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split())


def test_sl001_declares_normative_maturation_boundary() -> None:
    content = normalized(spec_text())

    assert "Normative Maturation Boundary" in content

    assert "normative maturation" in content.lower()

    for boundary in (
        "Promotion Eligibility",
        "Promotion Gate",
        "Version Authority",
    ):
        assert boundary in content

def test_sl001_declares_backward_transition_semantics() -> None:
    content = normalized(spec_text())

    assert "Backward Transitions" in content
    assert "backward transition" in content.lower()
    assert "Evidence" in content


def test_lifecycle_minimality_is_declared() -> None:
    content = normalized(spec_text())

    assert "Minimality Rule" in content
    assert "minimal" in content.lower()
    assert "Organizational convenience" in content


def test_freeze_declares_all_fifteen_invariants() -> None:
    content = freeze_text()

    identifiers = re.findall(
        r"^SLI-(\d{3})$",
        content,
        flags=re.MULTILINE,
    )

    required = {
        f"{i:03d}"
        for i in range(1, 16)
    }

    assert required.issubset(set(identifiers))
    assert set(identifiers).issubset(required)


def test_promotion_eligibility_is_external() -> None:
    content = normalized(spec_text())

    assert "Promotion Eligibility Interface" in content
    assert (
        "Promotion Eligibility is the first external "
        "interface after successful normative maturation."
        in content
    )


def test_implementation_independence_is_declared() -> None:
    content = normalized(spec_text())

    assert "Implementation Independence" in content

    for technology in (
        "Python",
        "Rust",
        "OpenCV",
        "CUDA",
        "ONNX",
        "WASM",
        "Docker",
    ):
        assert technology in content


def test_promotion_gate_is_external() -> None:
    content = normalized(spec_text())

    assert "Promotion Gate Interface" in content
    assert "Promotion Gate is external to SL-001." in content


def test_version_authority_is_external() -> None:
    content = normalized(spec_text())

    assert "Version Authority Interface" in content
    assert "Version Authority is external to SL-001." in content


def test_verification_is_not_lifecycle_state() -> None:
    content = normalized(spec_text())

    assert "Verification Boundary" in content
    assert "Verification is not a lifecycle state." in content


def test_contract_is_not_lifecycle_state() -> None:
    content = normalized(spec_text())

    assert "Executable Contract Boundary" in content
    assert (
        "Executable Contracts are not "
        "Specification Lifecycle states."
        in content
    )


def test_implementation_is_not_lifecycle_state() -> None:
    content = normalized(spec_text())

    assert "Implementation Boundary" in content
    assert (
        "Implementation is not "
        "a Specification Lifecycle state."
        in content
    )


def test_validation_is_not_lifecycle_state() -> None:
    content = normalized(spec_text())

    assert "Validation Boundary" in content
    assert (
        "Validation is not "
        "a Specification Lifecycle state."
        in content
    )


def test_versioning_is_not_lifecycle_state() -> None:
    content = normalized(spec_text())

    assert "Versioning Boundary" in content


def test_sl001_declares_all_fifteen_invariants() -> None:
    content = spec_text()

    identifiers = re.findall(
        r"^SLI-(\d{3})$",
        content,
        flags=re.MULTILINE,
    )

    assert identifiers == [
        f"{i:03d}"
        for i in range(1, 16)
    ]


def test_sli001_trigger_traceability() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-001 Every lifecycle instance shall have "
        "a traceable trigger."
        in content
    )


def test_sli002_investigation_precedes_specification() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-002 Investigation shall precede "
        "normative specification."
        in content
    )


def test_sli003_candidate_precedes_review() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-003 A candidate specification shall exist "
        "before Normative Review."
        in content
    )


def test_sli004_review_and_refutation_are_distinct() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-004 Normative Review and Refutation "
        "shall remain semantically distinct."
        in content
    )


def test_sli005_evidence_may_force_backward_transition() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-005 Evidence may force backward transition."
        in content
    )


def test_normative_authority_boundaries_are_declared() -> None:
    content = normalized(spec_text())

    for requirement in (
        "SLI-006 Implementation shall not create "
        "normative authority.",
        "SLI-007 Verification shall not create "
        "normative authority.",
        "SLI-008 Tests shall not create "
        "normative authority.",
        "SLI-009 Lifecycle completion shall not create "
        "normative authority.",
    ):
        assert requirement in content


def test_external_promotion_boundaries_are_declared() -> None:
    content = normalized(spec_text())

    for requirement in (
        "SLI-010 Promotion Eligibility shall remain "
        "external to the lifecycle.",
        "SLI-011 Promotion Gate shall remain "
        "external to the lifecycle.",
        "SLI-012 Version Authority shall remain "
        "external to the lifecycle.",
    ):
        assert requirement in content


def test_parallel_version_semantics_are_declared() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-013 Different specification versions may "
        "exist in different lifecycle conditions simultaneously."
        in content
    )


def test_historical_evidence_is_preserved() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-014 Historical evidence shall remain "
        "traceable after lifecycle exit."
        in content
    )


def test_new_evidence_reenters_through_trigger() -> None:
    content = normalized(spec_text())

    assert (
        "SLI-015 New normative evidence shall re-enter "
        "the lifecycle through a traceable trigger."
        in content
    )


def test_refutation_history_is_declared() -> None:
    content = normalized(spec_text())

    assert "Refutation History" in content

    for cycle in (
        "Cycle 1",
        "Cycle 2",
        "Cycle 3",
    ):
        assert cycle in content


def test_refutation_cycle_1_exists() -> None:
    assert (
        REFUTATION_DIR / "SL001_REFUTATION.md"
    ).is_file()


def test_refutation_cycle_2_exists() -> None:
    assert (
        REFUTATION_DIR / "SL001_REFUTATION_CYCLE_2.md"
    ).is_file()


def test_refutation_cycle_3_exists() -> None:
    assert (
        REFUTATION_DIR / "SL001_REFUTATION_CYCLE_3.md"
    ).is_file()


def test_adversarial_refutation_cycle_4_exists() -> None:
    assert (
        REFUTATION_DIR
        / "SL001_REFUTATION_CYCLE_4_ADVERSARIAL.md"
    ).is_file()


def test_freeze_targets_sl001_baseline_1_0() -> None:
    content = normalized(freeze_text())

    assert "SL-001-FREEZE" in content
    assert "Target Specification SL-001 Baseline 1.0" in content


def test_freeze_declares_permitted_changes() -> None:
    content = normalized(freeze_text())

    assert "Permitted Changes" in content
    assert "Typographical correction." in content
    assert "Formatting correction." in content


def test_freeze_declares_prohibited_changes() -> None:
    content = normalized(freeze_text())

    assert "Prohibited Changes" in content

    for requirement in (
        "Adding a sixth lifecycle state.",
        "Removing a frozen state.",
        "Collapsing Review and Refutation.",
        "Moving Promotion Eligibility inside the lifecycle.",
        "Moving Promotion Gate inside the lifecycle.",
        "Moving Version Authority inside the lifecycle.",
    ):
        assert requirement in content


def test_freeze_declares_breaking_evolution() -> None:
    content = normalized(freeze_text())

    assert "Breaking Evolution" in content

    for requirement in (
        "A new Trigger.",
        "New investigation.",
        "New canonical specification.",
        "New review.",
        "New refutation.",
        "A new Promotion Gate.",
        "A new normative version.",
    ):
        assert requirement in content


def test_freeze_declares_release_criteria() -> None:
    content = normalized(freeze_text())

    assert "Release Criteria" in content
    assert "All five canonical states are present." in content
    assert "All fifteen Lifecycle Invariants are present." in content
    assert "The executable foundation contract passes." in content


def test_freeze_declares_conformance() -> None:
    content = normalized(freeze_text())

    assert "Conformance" in content
    assert (
        "Conformance requires preservation of the frozen "
        "maturation semantics and authority boundaries."
        in content
    )


def test_freeze_declares_frozen_authority() -> None:
    content = normalized(freeze_text())

    assert "Freeze Status FROZEN." in content
    assert "Authority Target SL-001 Baseline 1.0." in content


def test_no_forbidden_lifecycle_states_are_reintroduced() -> None:
    content = spec_text()

    forbidden = (
        "BASELINED",
        "VERIFYING",
        "IMPLEMENTING",
        "VALIDATING",
        "EVOLVING",
        "RETIRED",
        "CANDIDATE_FOR_BASELINE",
    )

    for state in forbidden:
        assert not re.search(
            rf"^# State .*{state}",
            content,
            flags=re.MULTILINE,
        )


def test_sl001_end_marker() -> None:
    assert spec_text().rstrip().endswith(
        "# End of Specification"
    )


def test_sl001_freeze_end_marker() -> None:
    assert freeze_text().rstrip().endswith(
        "# End of Specification Freeze"
    )
