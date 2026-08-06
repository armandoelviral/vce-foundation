"""
Executable Specification

CKP-007.22
Commerce Reasoning Replay Specification Freeze
"""

from __future__ import annotations

from pathlib import Path


SPEC = (
    Path(__file__).resolve().parents[2]
    / "research"
    / "commerce"
    / "reasoning_replay"
    / "CKP007_SPECIFICATION_FREEZE.md"
)

EXPECTED_SECTIONS = (
    "## Purpose",
    "## Normative Dependencies",
    "## Specification Freeze Identity",
    "## Specification Freeze Version",
    "## Specification Freeze Lifecycle",
    "## Specification Freeze Scope",
    "## Frozen Specification Set",
    "## Frozen Executable Contracts",
    "## Frozen Normative Boundaries",
    "## Frozen Compatibility",
    "## Evolution Policy",
    "## Allowed Changes",
    "## Prohibited Changes",
    "## Release Criteria",
    "## Conformance Requirements",
    "## Read-Only Historical Boundary",
    "## Specification Freeze Invariants",
    "## Release Boundary",
    "## Next Deliverable",
)

LIFECYCLE = (
    "Created.",
    "Approved.",
    "Released.",
    "Frozen.",
)

FROZEN_SPECS = tuple(f"CKP-007.{i}" for i in range(1, 22))

CENTRAL_RULES = (
    "Specification Freeze shall preserve CKP-007 Baseline 1.0.",
    "Specification Freeze shall preserve all normative specifications.",
    "Specification Freeze shall preserve all executable specification contracts.",
    "Specification Freeze shall preserve all canonical section ordering.",
    "Specification Freeze shall preserve all normative invariants.",
    "Specification Freeze shall preserve all compatibility guarantees.",
    "Specification Freeze shall remain deterministic.",
    "Specification Freeze shall remain immutable.",
    "Specification Freeze shall fail closed.",
)

ALLOWED_CHANGES = (
    "New CKP specification families.",
    "New major versions.",
    "New executable contracts.",
    "Normative extensions.",
    "Informative annexes.",
    "Editorial clarifications that do not modify normative meaning.",
    "Documentation improvements that do not modify normative meaning.",
)

PROHIBITED_CHANGES = (
    "Changing frozen identities.",
    "Changing frozen versions.",
    "Changing canonical section ordering.",
    "Changing lifecycle definitions.",
    "Changing status definitions.",
    "Changing normative relationships.",
    "Changing normative cardinality.",
    "Changing normative dependencies.",
    "Changing normative compatibility.",
    "Changing normative invariants.",
    "Changing canonical serialization.",
    "Changing deterministic ordering.",
    "Changing executable contracts.",
    "Changing read-only historical boundaries.",
    "Retrospective modification of CKP-007 Baseline 1.0.",
    "Normative reinterpretation.",
    "Silent behavioral changes.",
    "Partial freeze replacement.",
)

INVARIANTS = (
    "Exactly one Specification Freeze Identity.",
    "Exactly one Baseline Version.",
    "Exactly one Frozen Specification Set.",
    "Exactly one Frozen Executable Contract Set.",
    "Identity Preservation.",
    "Baseline Preservation.",
    "Compatibility Preservation.",
    "Contract Preservation.",
    "Relationship Preservation.",
    "Invariant Preservation.",
    "Serialization Preservation.",
    "Deterministic Ordering Preservation.",
    "Read-Only Preservation.",
    "Fail-Closed Freeze.",
)


def spec_text() -> str:
    return SPEC.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(spec_text().split())


def headings() -> list[str]:
    return [
        line
        for line in spec_text().splitlines()
        if line.startswith("## ")
    ]


def test_document_exists() -> None:
    assert SPEC.is_file()


def test_document_not_empty() -> None:
    assert SPEC.stat().st_size > 0


def test_identity() -> None:
    content = normalized_text()

    assert "# CKP-007" in content
    assert "Title Commerce Reasoning Replay Specification Freeze" in content
    assert "Abbreviation CRSF" in content
    assert "Version 1.0" in content
    assert "Status Draft" in content


def test_sections_exist_once() -> None:
    hs = headings()

    for section in EXPECTED_SECTIONS:
        assert hs.count(section) == 1, section


def test_section_order() -> None:
    assert tuple(headings()) == EXPECTED_SECTIONS


def test_lifecycle() -> None:
    content = normalized_text()

    for state in LIFECYCLE:
        assert state in content

    assert "Lifecycle regression is prohibited." in content
    assert "Terminal lifecycle states shall remain immutable." in content


def test_frozen_specification_set() -> None:
    content = normalized_text()

    for spec in FROZEN_SPECS:
        assert spec in content

    assert (
        "Frozen Specification Set shall remain immutable."
        in content
    )


def test_frozen_contracts() -> None:
    content = normalized_text()

    assert (
        "Every executable specification contract associated with "
        "CKP-007.1 through CKP-007.21 is frozen."
        in content
    )

    assert (
        "Frozen executable contracts shall remain immutable."
        in content
    )

    assert (
        "Executable contract behavior shall not change under this Baseline."
        in content
    )


def test_central_rules() -> None:
    content = normalized_text()

    for rule in CENTRAL_RULES:
        assert rule in content


def test_frozen_boundaries() -> None:
    content = normalized_text()

    for item in (
        "Normative identities.",
        "Normative versions.",
        "Canonical section ordering.",
        "Normative relationships.",
        "Normative dependencies.",
        "Normative compatibility.",
        "Normative invariants.",
        "Canonical serialization.",
        "Deterministic ordering.",
        "Executable specification contracts.",
    ):
        assert item in content


def test_compatibility() -> None:
    content = normalized_text()

    assert "CKP-005 Baseline 1.0." in content
    assert "CKP-006 Baseline 1.0." in content

    for spec in FROZEN_SPECS:
        assert spec in content


def test_evolution_policy() -> None:
    content = normalized_text()

    for rule in (
        "Future versions may:",
        "Add new CKP families.",
        "Add new specifications.",
        "Add new executable contracts.",
        "Future versions shall never modify CKP-007 Baseline 1.0.",
        "Future versions shall remain backward compatible with CKP-007 Baseline 1.0.",
    ):
        assert rule in content


def test_allowed_changes() -> None:
    content = normalized_text()

    for change in ALLOWED_CHANGES:
        assert change in content


def test_prohibited_changes() -> None:
    content = normalized_text()

    for change in PROHIBITED_CHANGES:
        assert change in content


def test_release_criteria() -> None:
    content = normalized_text()

    for criterion in (
        "All normative specifications are present.",
        "All executable specification contracts pass successfully.",
        "The complete CKP-007 regression suite passes.",
        "Compatibility is fully preserved.",
        "Release shall fail when any mandatory criterion is not satisfied.",
    ):
        assert criterion in content


def test_conformance() -> None:
    content = normalized_text()

    for requirement in (
        "Conformance shall never be partial.",
        "Partial conformance shall fail validation.",
        "Conformance shall remain deterministic.",
    ):
        assert requirement in content


def test_read_only_boundary() -> None:
    content = normalized_text()

    for target in (
        "Frozen Specifications.",
        "Frozen Executable Contracts.",
        "Frozen Relationships.",
        "Frozen Dependencies.",
        "Frozen Compatibility.",
        "Frozen Baseline.",
    ):
        assert target in content

    assert (
        "Specification Freeze shall never modify, reinterpret, normalize, "
        "repair, replace, merge, or suppress frozen normative artifacts."
        in content
    )


def test_invariants() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_boundary() -> None:
    content = normalized_text()

    assert "Version 1.0 freezes completely:" in content

    for spec in FROZEN_SPECS:
        assert spec in content

    assert (
        "Future CKP specifications shall preserve this Specification Freeze."
        in content
    )


def test_next_deliverable() -> None:
    content = normalized_text()

    assert "CKP-008" in content
    assert "Reserved." in content


def test_end_marker() -> None:
    text = spec_text()

    assert text.count("# End of Specification") == 1
    assert text.rstrip().endswith("# End of Specification")
