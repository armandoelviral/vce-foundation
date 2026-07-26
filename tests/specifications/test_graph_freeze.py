from pathlib import Path


FREEZE = Path(
    "research/commerce/releases/"
    "CKP_GRAPH_FREEZE_v1.0.0.md"
)


FROZEN_COMPONENTS = (
    "Canonical Vocabulary.",
    "Vocabulary Registry.",
    "Canonical Definitions.",
    "Preferred Names.",
    "Forbidden Synonyms.",
    "Commerce Ontology.",
    "Ontology Assertions.",
    "Relationship Types.",
    "Graph Structure.",
    "Graph Nodes.",
    "Graph Edges.",
    "Traversal Model.",
    "Registered Paths.",
    "Consistency Audit.",
    "Integrity References.",
    "Deterministic Ordering.",
    "Validation Evidence.",
)


COMPATIBILITY_RULES = (
    "Backward compatibility shall be verified.",
    "Vocabulary compatibility shall be verified.",
    "Ontology compatibility shall be verified.",
    "Graph compatibility shall be verified.",
    "Deterministic behavior shall be preserved.",
    "Compatibility verification shall be repeatable.",
)


ALLOWED_EVOLUTION = (
    "Add new Canonical Terms.",
    "Add new Ontology Assertions.",
    "Add new Graph Nodes.",
    "Add new Graph Edges.",
    "Add new Traversal Capabilities.",
    "Add new Query Capabilities.",
    "Add new Evidence Types.",
    "Add new Graph Services.",
)


FORBIDDEN_CHANGES = (
    "Changing Canonical Identifiers.",
    "Changing Preferred Names.",
    "Changing Canonical Definitions.",
    "Changing Relationship Identifiers.",
    "Changing Relationship Types.",
    "Changing Graph Identifiers.",
    "Changing Graph Integrity References.",
    "Changing deterministic ordering.",
    "Removing frozen Graph Nodes.",
    "Removing frozen Graph Edges.",
    "Removing frozen Vocabulary Terms.",
    "Removing frozen Ontology Assertions.",
    "Reinterpreting frozen semantics.",
    "Silent compatibility breaks.",
    "Private semantic extensions.",
    "In-place mutation of frozen artifacts.",
)


FREEZE_INVARIANTS = (
    "Foundation Compatibility.",
    "Specification Runtime Compatibility.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Knowledge Graph Compatibility.",
    "Canonical Identity Preservation.",
    "Deterministic Ordering Preservation.",
    "Graph Integrity Preservation.",
    "Semantic Preservation.",
    "Traceability Preservation.",
    "Backward Compatibility.",
    "Immutable Baseline Preservation.",
    "Fail-Closed Governance.",
)


def freeze_text() -> str:
    return FREEZE.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        freeze_text().split()
    )


def test_freeze_document_exists() -> None:
    assert FREEZE.is_file()


def test_document_identity() -> None:
    content = normalized_text()

    assert (
        "Commerce Knowledge Graph Freeze"
        in content
    )

    assert "Version 1.0.0" in content

    assert "Status Frozen" in content

    assert "Release Identifier CKP-003.8" in content


def test_purpose_is_declared() -> None:
    content = normalized_text()

    assert (
        "Declare the Commerce Knowledge Graph Version "
        "1.0 as an immutable normative baseline."
    ) in content

    assert (
        "The frozen baseline shall be consumed by "
        "future Commerce capabilities without "
        "modifying its normative behavior."
    ) in content


def test_freeze_declaration_exists() -> None:
    content = normalized_text()

    for rule in (
        "Commerce Knowledge Graph Version 1.0 is "
        "hereby declared Frozen.",
        "The frozen Graph becomes the normative "
        "Commerce Knowledge Graph baseline.",
        "Every future Commerce capability shall "
        "consume this baseline.",
        "No future capability may redefine this "
        "baseline in-place.",
    ):
        assert rule in content


def test_immutable_baseline_is_declared() -> None:
    content = normalized_text()

    for baseline in (
        "CKP-001 Canonical Commerce Vocabulary 1.0",
        "CKP-002 Commerce Ontology 1.0",
        "CKP-003 Commerce Knowledge Graph 1.0",
    ):
        assert baseline in content

    assert (
        "The baseline shall remain immutable."
    ) in content


def test_frozen_components_are_declared() -> None:
    content = freeze_text()

    for component in FROZEN_COMPONENTS:
        assert component in content

    assert (
        "No frozen component may be modified "
        "in-place."
    ) in normalized_text()


def test_compatibility_rules_are_declared() -> None:
    content = normalized_text()

    for rule in COMPATIBILITY_RULES:
        assert rule in content


def test_allowed_evolution_is_declared() -> None:
    content = freeze_text()

    for capability in ALLOWED_EVOLUTION:
        assert capability in content

    normalized = normalized_text()

    assert (
        "Every addition shall preserve compatibility "
        "with Version 1.0."
    ) in normalized

    assert (
        "No addition may invalidate frozen semantics."
    ) in normalized


def test_forbidden_changes_are_declared() -> None:
    content = freeze_text()

    for prohibition in FORBIDDEN_CHANGES:
        assert prohibition in content


def test_governance_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "The Commerce Knowledge Graph shall evolve "
        "under formal governance.",
        "Every normative modification shall be "
        "reviewed.",
        "Every normative modification shall be "
        "traceable.",
        "Every normative modification shall be "
        "auditable.",
        "Governance decisions shall remain publicly "
        "documented.",
    ):
        assert rule in content


def test_adr_requirement_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "Architectural justification.",
        "An approved Architecture Decision Record.",
        "Impact analysis.",
        "Compatibility analysis.",
        "Traceability analysis.",
        "Evidence generation.",
    ):
        assert requirement in content

    assert (
        "No architectural modification may bypass "
        "the ADR process."
    ) in content


def test_regression_requirement_is_declared() -> None:
    content = normalized_text()

    assert (
        "Every normative modification requires a "
        "full regression suite."
    ) in content

    for suite in (
        "Vocabulary regression.",
        "Ontology regression.",
        "Knowledge Graph regression.",
        "Traversal regression.",
        "Consistency Audit regression.",
        "Specification regression.",
        "Runtime regression.",
    ):
        assert suite in freeze_text()

    assert (
        "No modification shall be accepted when "
        "any mandatory regression fails."
    ) in content


def test_versioning_policy_is_declared() -> None:
    content = normalized_text()

    for rule in (
        "Semantic Versioning shall govern releases.",
        "Patch releases:",
        "Minor releases:",
        "Major releases:",
        "Version 1.0 shall remain permanently "
        "available.",
    ):
        assert rule in content


def test_freeze_invariants_are_declared() -> None:
    content = freeze_text()

    for invariant in FREEZE_INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Freeze Declaration is declared.",
        "Immutable Baseline is declared.",
        "Frozen Components are declared.",
        "Compatibility Rules are declared.",
        "Allowed Evolution is declared.",
        "Forbidden Changes are declared.",
        "Governance is declared.",
        "ADR Requirement is declared.",
        "Regression Requirement is declared.",
        "Versioning Policy is declared.",
        "Freeze Invariants are declared.",
        "Commerce Knowledge Graph Version 1.0 is "
        "officially frozen.",
    ):
        assert criterion in content


def test_effectivity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Effective immediately."
    ) in content

    assert (
        "This Freeze remains valid until superseded "
        "by a future major version."
    ) in content

    assert (
        "Version 1.0 shall remain available for "
        "verification, replay, compatibility analysis, "
        "and historical audit."
    ) in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004" in content

    assert (
        "Commerce Query Language."
    ) in content
