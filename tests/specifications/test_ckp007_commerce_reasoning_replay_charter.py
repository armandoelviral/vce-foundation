"""
Executable Specification

CKP-007.1
Commerce Reasoning Replay Charter
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_COMMERCE_REASONING_REPLAY_CHARTER.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Replay Identity",
    "## Replay Mission",
    "## Normative Baseline",
    "## Replay Scope",
    "## Replay Responsibilities",
    "## Replay Non-Responsibilities",
    "## Historical Execution Boundary",
    "## Artifact Resolution Boundary",
    "## Environment Reconstruction Boundary",
    "## Determinism",
    "## Fail-Closed Behavior",
    "## Read-Only Historical Boundary",
    "## Replay Lifecycle",
    "## Replay Inputs",
    "## Replay Outputs",
    "## Replay Evidence",
    "## Replay Integrity",
    "## Replay Comparison",
    "## Divergence Semantics",
    "## Failure Semantics",
    "## Security Boundary",
    "## Conformance Requirements",
    "## Success Criteria",
    "## Release Boundary",
    "## Next Deliverable",
)

REPLAY_LIFECYCLE_STATES = (
    "Created.",
    "Initialized.",
    "Reconstructed.",
    "Validated.",
    "Compared.",
    "Completed.",
    "Archived.",
)

REPLAY_RESPONSIBILITIES = (
    "Resolve historical artifacts.",
    "Reconstruct Runtime context.",
    "Reconstruct Runtime state.",
    "Reconstruct Runtime stages.",
    "Reconstruct Runtime transitions.",
    "Preserve deterministic ordering.",
    "Produce Replay Evidence.",
    "Produce Replay Result.",
    "Detect divergence.",
    "Preserve integrity.",
    "Preserve traceability.",
)

REPLAY_NON_RESPONSIBILITIES = (
    "Execute new business logic.",
    "Modify Runtime behavior.",
    "Modify historical artifacts.",
    "Repair historical artifacts.",
    "Rewrite historical history.",
    "Interpret missing information.",
    "Introduce implicit assumptions.",
)

REPLAY_INPUTS = (
    "Replay Request.",
    "Historical Runtime Execution.",
    "Historical Runtime Result.",
    "Historical Artifact Registry.",
    "Historical Runtime Configuration.",
    "Historical Runtime Limits.",
    "Frozen Baselines.",
)

REPLAY_OUTPUTS = (
    "Replay Result.",
    "Replay Evidence.",
    "Replay Comparison.",
    "Replay Validation Result.",
    "Replay Divergence Report when applicable.",
    "Replay Traceability.",
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
    assert "Title Commerce Reasoning Replay Charter" in content
    assert "Abbreviation CRRC" in content
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


def test_no_unexpected_level_two_headings_exist() -> None:
    assert tuple(level_two_headings()) == EXPECTED_SECTIONS


def test_purpose_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Define the canonical, deterministic, immutable, "
        "fail-closed, traceable, replay-compatible, and "
        "integrity-preserving Commerce Reasoning Replay.",
        "Replay reconstructs exactly one historical Runtime Execution.",
        "Replay shall reproduce the historical Reasoning process "
        "without altering the historical record.",
        "This specification establishes the mission, scope, "
        "boundaries, lifecycle, integrity, comparison, and "
        "governance of Replay.",
        "This specification introduces no Runtime execution behavior.",
    ):
        assert requirement in content


def test_replay_identity_is_unique_and_immutable() -> None:
    content = normalized_text()

    for requirement in (
        "Every Replay shall possess exactly one immutable "
        "Replay Identifier.",
        "CKP-REPLAY-000001",
        "Replay Identity shall be globally unique.",
        "Replay Identity shall never be reused.",
        "Missing, malformed, duplicated, or reused Replay "
        "Identity shall fail validation.",
    ):
        assert requirement in content


def test_replay_mission_is_declared() -> None:
    content = normalized_text()

    for mission in (
        "Replay shall reconstruct exactly one historical "
        "Runtime Execution.",
        "Replay shall reproduce deterministic Reasoning behavior.",
        "Replay shall verify historical consistency.",
        "Replay shall preserve historical evidence.",
        "Replay shall preserve traceability.",
        "Replay shall detect divergence.",
        "Replay shall produce a Replay Result.",
    ):
        assert mission in content


def test_normative_baseline_is_frozen_and_immutable() -> None:
    content = normalized_text()

    for baseline in (
        "CKP-005 Baseline 1.0.",
        "CKP-005 Specification Freeze.",
        "CKP-006 Baseline 1.0.",
        "CKP-006 Specification Freeze.",
    ):
        assert baseline in content

    assert (
        "Replay shall execute only against frozen baselines."
    ) in content
    assert "Normative baselines shall remain immutable." in content


def test_replay_scope_is_exactly_one_historical_execution() -> None:
    content = normalized_text()

    for requirement in (
        "Replay applies to exactly one historical Runtime Execution.",
        "Replay shall consume only versioned historical artifacts.",
        "Replay shall reconstruct the historical execution environment.",
        "Replay shall not extend beyond the selected "
        "historical execution.",
    ):
        assert requirement in content


def test_replay_responsibilities_are_declared() -> None:
    content = normalized_text()

    for responsibility in REPLAY_RESPONSIBILITIES:
        assert responsibility in content


def test_replay_non_responsibilities_are_declared() -> None:
    content = normalized_text()

    for prohibition in REPLAY_NON_RESPONSIBILITIES:
        assert prohibition in content


def test_historical_execution_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay shall reconstruct exactly one historical "
        "Runtime Execution.",
        "Historical Execution boundaries shall remain immutable.",
        "Replay shall never merge multiple historical executions.",
    ):
        assert requirement in content


def test_artifact_resolution_boundary_is_closed() -> None:
    content = normalized_text()

    for requirement in (
        "Replay shall resolve only frozen, versioned, "
        "registered artifacts.",
        "Unregistered artifacts shall fail validation.",
        "Replay shall never synthesize artifacts.",
    ):
        assert requirement in content


def test_environment_reconstruction_boundary_is_explicit() -> None:
    content = normalized_text()

    for reconstructed_item in (
        "Runtime.",
        "Baseline.",
        "Artifact Registry.",
        "Configuration.",
        "Limits.",
    ):
        assert reconstructed_item in content

    assert (
        "Replay shall not use implicit environmental state."
    ) in content
    assert (
        "Replay shall not depend upon external mutable state."
    ) in content


def test_replay_is_deterministic() -> None:
    content = normalized_text()

    for requirement in (
        "Replay shall be deterministic.",
        "Replay shall preserve canonical ordering.",
        "Replay shall preserve deterministic resolution.",
        "Equivalent Replay executions shall produce equivalent "
        "Replay Results.",
        "Implementation-defined behavior is prohibited.",
    ):
        assert requirement in content


def test_replay_fails_closed() -> None:
    content = normalized_text()

    for requirement in (
        "Replay validation shall fail closed.",
        "Missing artifacts shall fail validation.",
        "Missing evidence shall fail validation.",
        "Baseline mismatch shall fail validation.",
        "Integrity mismatch shall fail validation.",
        "Environment mismatch shall fail validation.",
    ):
        assert requirement in content


def test_historical_boundary_is_read_only() -> None:
    content = normalized_text()

    for historical_artifact in (
        "Historical Runtime Execution.",
        "Historical Runtime State.",
        "Historical Runtime Result.",
        "Historical Artifact Registry.",
        "Historical Evidence.",
        "Historical Proofs.",
        "Historical Facts.",
        "Historical Premises.",
        "Historical Rules.",
        "Frozen Baselines.",
    ):
        assert historical_artifact in content

    assert "Replay shall not modify:" in content


def test_replay_lifecycle_is_declared() -> None:
    content = normalized_text()

    for lifecycle_state in REPLAY_LIFECYCLE_STATES:
        assert lifecycle_state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_replay_inputs_are_declared() -> None:
    content = normalized_text()

    for replay_input in REPLAY_INPUTS:
        assert replay_input in content


def test_replay_outputs_are_declared() -> None:
    content = normalized_text()

    for replay_output in REPLAY_OUTPUTS:
        assert replay_output in content


def test_replay_evidence_is_complete_and_immutable() -> None:
    content = normalized_text()

    for evidence_type in (
        "Historical references.",
        "Reconstruction evidence.",
        "Validation evidence.",
        "Comparison evidence.",
        "Integrity evidence.",
    ):
        assert evidence_type in content

    assert "Evidence shall remain immutable." in content


def test_replay_integrity_is_declared() -> None:
    content = normalized_text()

    for preserved_property in (
        "Identity.",
        "Historical artifact integrity.",
        "Deterministic ordering.",
        "Canonical serialization.",
        "Traceability.",
    ):
        assert preserved_property in content

    assert "Mutation shall invalidate Replay Integrity." in content


def test_replay_comparison_is_deterministic() -> None:
    content = normalized_text()

    for comparison_target in (
        "Historical Runtime Result.",
        "Reconstructed Runtime Result.",
        "Historical Evidence.",
        "Reconstructed Evidence.",
        "Historical Conclusions.",
        "Reconstructed Conclusions.",
    ):
        assert comparison_target in content

    assert "Comparison shall be deterministic." in content


def test_divergence_semantics_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay shall detect divergence.",
        "Equivalent executions shall not diverge.",
        "Every detected divergence shall be explicit.",
        "Every divergence shall be traceable.",
        "Unexplained divergence shall fail validation.",
    ):
        assert requirement in content


def test_failure_semantics_are_declared() -> None:
    content = normalized_text()

    for failure_condition in (
        "Historical artifacts are missing.",
        "Historical artifacts are invalid.",
        "Integrity verification fails.",
        "Replay validation fails.",
        "Replay comparison fails.",
        "Deterministic ordering fails.",
        "Canonical serialization fails.",
        "Historical environment cannot be reconstructed.",
    ):
        assert failure_condition in content


def test_security_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Replay shall operate exclusively on trusted "
        "historical artifacts.",
        "Replay shall preserve immutable baselines.",
        "Replay shall preserve artifact integrity.",
        "Replay shall never bypass validation.",
        "Replay shall never trust implicit state.",
    ):
        assert requirement in content


def test_conformance_requirements_are_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Preserve Replay Identity.",
        "Preserve deterministic behavior.",
        "Preserve historical integrity.",
        "Preserve traceability.",
        "Preserve replay compatibility.",
        "Pass Replay validation.",
        "Respect frozen baselines.",
        "Operate fail-closed.",
    ):
        assert requirement in content


def test_success_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Exactly one historical execution is reconstructed.",
        "Historical artifacts resolve successfully.",
        "Historical environment is reconstructed.",
        "Validation succeeds.",
        "Comparison succeeds.",
        "No unexplained divergence exists.",
        "Integrity is preserved.",
        "Traceability is preserved.",
        "Replay Result is produced.",
        "Replay Evidence is produced.",
    ):
        assert criterion in content


def test_release_boundary_is_declared() -> None:
    content = normalized_text()

    for included_capability in (
        "Replay Identity.",
        "Replay Mission.",
        "Replay Scope.",
        "Replay Responsibilities.",
        "Replay Boundaries.",
        "Replay Lifecycle.",
        "Replay Inputs.",
        "Replay Outputs.",
        "Replay Evidence.",
        "Replay Integrity.",
        "Replay Comparison.",
        "Divergence Semantics.",
        "Failure Semantics.",
        "Security Boundary.",
        "Conformance Requirements.",
    ):
        assert included_capability in content

    for excluded_capability in (
        "Replay engine implementation.",
        "Persistence.",
        "WAL.",
        "Event sourcing.",
        "Schedulers.",
        "Concurrency.",
        "Distributed infrastructure.",
        "Cryptographic algorithms.",
        "Implementation classes.",
    ):
        assert excluded_capability in content

    assert (
        "Future CKP-007 specifications shall preserve this Charter."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-007.2" in content
    assert "Replay Structure Model." in content


def test_end_marker_is_unique_and_final() -> None:
    content = spec_text()

    assert content.count("# End of Specification") == 1
    assert content.rstrip().endswith("# End of Specification")
