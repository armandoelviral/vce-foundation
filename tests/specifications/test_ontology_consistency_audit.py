from pathlib import Path


AUDIT = Path(
    "research/commerce/ontology/audits/"
    "ONTOLOGY_CONSISTENCY_AUDIT.md"
)

AUDIT_AREAS = (
    "Ontology Nodes.",
    "Canonical Identifiers.",
    "Ontology Classes.",
    "Root Node.",
    "Hierarchy Assertions.",
    "Relationship Assertions.",
    "Directionality.",
    "Inverse Relationships.",
    "Domain Membership.",
    "Registry Closure.",
    "Vocabulary Compatibility.",
    "Ontology Invariants.",
    "Audit Evidence.",
)

ONTOLOGY_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Vocabulary Compatibility.",
    "Registered Object Closure.",
    "Single Root Preservation.",
    "Hierarchy Acyclicity.",
    "Relationship Direction Preservation.",
    "Inverse Relationship Consistency.",
    "No Duplicate Assertions.",
    "Domain Separation.",
    "Semantic Closure.",
    "Traceability Closure.",
)

ACCEPTANCE_CRITERIA = (
    "Exactly ten registered Ontology Nodes exist.",
    "Commerce is the only root Ontology Node.",
    "Every node preserves canonical identity.",
    "Every hierarchy assertion is explicit and acyclic.",
    "Every relationship assertion uses a canonical relationship type.",
    "Every inverse-paired assertion is consistent.",
    "Every node belongs to the Knowledge Registry.",
    "No private canonical redefinition exists.",
    "No duplicate semantic assertion exists.",
    "All Ontology Invariants are satisfied.",
)


def audit_text() -> str:
    return AUDIT.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        audit_text().split()
    )


def test_ontology_consistency_audit_exists() -> None:
    assert AUDIT.is_file()


def test_audit_scope_is_complete() -> None:
    content = audit_text()

    for area in AUDIT_AREAS:
        assert area in content


def test_node_registration_audit_is_defined() -> None:
    content = normalized_text()

    assert (
        "Verify that every Ontology Node references "
        "one registered Canonical Commerce Term."
    ) in content

    assert (
        "Verify that no unregistered node exists."
    ) in content

    assert (
        "Verify that every Ontology Node preserves "
        "its Canonical Identifier."
    ) in content


def test_canonical_identity_audit_is_defined() -> None:
    content = normalized_text()

    assert (
        "Verify that every Ontology Node has one "
        "immutable Canonical Identifier."
    ) in content

    assert (
        "Verify that no private identifier replaces "
        "a Canonical Identifier."
    ) in content

    assert (
        "Verify that no Canonical Identifier is reused."
    ) in content


def test_root_node_audit_is_defined() -> None:
    content = normalized_text()

    assert (
        "Verify that Commerce is the only root "
        "Ontology Node."
    ) in content

    assert (
        "Verify that Commerce declares no parent "
        "inside the Initial Commerce Ontology."
    ) in content

    assert (
        "Verify that every non-root hierarchy node "
        "is reachable from Commerce through explicit "
        "Hierarchy Assertions."
    ) in content


def test_hierarchy_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Verify that every Hierarchy Assertion uses "
        "the canonical Is A relationship type.",
        "Verify that hierarchy direction is explicit.",
        "Verify that no node is its own ancestor.",
        "Verify that no circular hierarchy path exists.",
        "Verify that no duplicate parent-child "
        "assertion exists.",
    ):
        assert rule in content


def test_relationship_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Verify that every Relationship Assertion "
        "references registered Ontology Nodes.",
        "Verify that every Relationship Assertion uses "
        "one canonical Relationship Type.",
        "Verify that every Relationship Assertion "
        "declares directionality.",
        "Verify that duplicate semantic assertions do "
        "not exist.",
        "Verify that Related To is not used when a "
        "more specific relationship applies.",
    ):
        assert rule in content


def test_inverse_consistency_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Verify that every inverse-paired assertion "
        "references its inverse assertion.",
        "Verify that inverse-paired assertions preserve "
        "the same participating Ontology Nodes in "
        "reversed semantic direction.",
        "Verify that Part Of and Contains remain "
        "inverse-consistent.",
        "Verify that Uses and Used By remain "
        "inverse-consistent.",
    ):
        assert rule in content


def test_registry_closure_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Verify that all Ontology Nodes belong to the "
        "Knowledge Registry.",
        "Verify that all referenced Canonical "
        "Identifiers exist in the frozen CKP-001 "
        "baseline.",
        "Verify that no orphan Knowledge Object exists "
        "inside the Initial Commerce Ontology.",
    ):
        assert rule in content


def test_vocabulary_compatibility_audit_is_defined() -> None:
    content = normalized_text()

    for rule in (
        "Verify that Preferred Names match the frozen "
        "Canonical Commerce Vocabulary.",
        "Verify that canonical definitions are not "
        "privately redefined.",
        "Verify that Forbidden Synonyms are not used "
        "as Preferred Names.",
    ):
        assert rule in content


def test_ontology_invariants_are_audited() -> None:
    content = audit_text()

    for invariant in ONTOLOGY_INVARIANTS:
        assert invariant in content


def test_audit_evidence_is_defined() -> None:
    content = normalized_text()

    assert (
        "The audit shall produce deterministic and "
        "repeatable evidence."
    ) in content

    for field_name in (
        "Audit Rule.",
        "Validated Object.",
        "Validation Result.",
        "Failure Reason.",
        "Evidence Reference.",
    ):
        assert field_name in audit_text()


def test_acceptance_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in ACCEPTANCE_CRITERIA:
        assert criterion in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "All audit areas are verified.",
        "No semantic inconsistency remains open.",
        "No structural inconsistency remains open.",
        "No registry closure violation remains open.",
        "Ontology compatibility with CKP-001 is verified.",
        "The Initial Commerce Ontology is eligible for Freeze.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-002.8" in content
    assert "Commerce Ontology Freeze" in content
