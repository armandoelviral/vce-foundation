import re
from pathlib import Path


ONTOLOGY = Path(
    "research/commerce/ontology/"
    "INITIAL_COMMERCE_ONTOLOGY.md"
)

TERM_DIRECTORY = Path(
    "research/commerce/registry/terms"
)

CANONICAL_TERMS = {
    "CKP-TERM-000001": "Commerce",
    "CKP-TERM-000002": "Retail",
    "CKP-TERM-000003": "Wholesale",
    "CKP-TERM-000004": "Ecommerce",
    "CKP-TERM-000005": "Informal Commerce",
    "CKP-TERM-000006": "Product",
    "CKP-TERM-000007": "SKU",
    "CKP-TERM-000008": "Inventory",
    "CKP-TERM-000009": "Customer",
    "CKP-TERM-000010": "Channel",
}

HIERARCHY_ASSERTIONS = (
    "Retail Is A Commerce.",
    "Wholesale Is A Commerce.",
    "Ecommerce Is A Commerce.",
    "Informal Commerce Is A Commerce.",
)

SEMANTIC_ASSERTIONS = (
    "SKU Part Of Product.",
    "Product Contains SKU.",
    "Product Tracked As SKU.",
    "Retail Uses Channel.",
    "Channel Used By Retail.",
    "Product Sold Through Channel.",
    "Inventory Applies To SKU.",
    "Customer Uses Channel.",
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


def ontology_text() -> str:
    return ONTOLOGY.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        ontology_text().split()
    )


def registered_term_ids() -> set[str]:
    return {
        path.name.split("_", maxsplit=1)[0]
        for path in TERM_DIRECTORY.glob(
            "CKP-TERM-*.md"
        )
    }


def ontology_node_ids() -> tuple[str, ...]:
    return tuple(
        re.findall(
            r"^### (CKP-TERM-\d{6})$",
            ontology_text(),
            flags=re.MULTILINE,
        )
    )


def relationship_ids() -> tuple[str, ...]:
    return tuple(
        re.findall(
            r"^### (CKP-REL-\d{6})$",
            ontology_text(),
            flags=re.MULTILINE,
        )
    )


def test_initial_ontology_exists() -> None:
    assert ONTOLOGY.is_file()


def test_initial_ontology_declares_exactly_ten_nodes() -> None:
    node_ids = ontology_node_ids()

    assert len(node_ids) == 10
    assert len(set(node_ids)) == 10


def test_every_initial_node_is_registered() -> None:
    assert set(ontology_node_ids()) == (
        registered_term_ids()
    )


def test_every_canonical_term_is_declared() -> None:
    content = ontology_text()

    for identifier, preferred_name in (
        CANONICAL_TERMS.items()
    ):
        assert identifier in content
        assert preferred_name in content


def test_no_unregistered_term_identifier_is_used() -> None:
    referenced_ids = set(
        re.findall(
            r"CKP-TERM-\d{6}",
            ontology_text(),
        )
    )

    assert referenced_ids <= registered_term_ids()


def test_commerce_is_the_only_root() -> None:
    content = normalized_text()

    assert (
        "Commerce is the root Ontology Node."
        in content
    )

    assert (
        "Commerce shall remain the only root node."
        in content
    )


def test_hierarchy_assertions_are_declared() -> None:
    content = normalized_text()

    for assertion in HIERARCHY_ASSERTIONS:
        assert assertion in content


def test_twelve_relationship_assertions_are_declared() -> None:
    identifiers = relationship_ids()

    assert len(identifiers) == 12
    assert len(set(identifiers)) == 12


def test_semantic_assertions_are_declared() -> None:
    content = normalized_text()

    for assertion in SEMANTIC_ASSERTIONS:
        assert assertion in content


def test_part_of_and_contains_are_inverse_paired() -> None:
    content = normalized_text()

    assert (
        "CKP-REL-000005 Source Node "
        "CKP-TERM-000007 Relationship Type "
        "Part Of Target Node CKP-TERM-000006"
    ) in content

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000006"
    ) in content

    assert (
        "CKP-REL-000006 Source Node "
        "CKP-TERM-000006 Relationship Type "
        "Contains Target Node CKP-TERM-000007"
    ) in content

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000005"
    ) in content


def test_uses_and_used_by_are_inverse_paired() -> None:
    content = normalized_text()

    assert (
        "CKP-REL-000008 Source Node "
        "CKP-TERM-000002 Relationship Type "
        "Uses Target Node CKP-TERM-000010"
    ) in content

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000009"
    ) in content

    assert (
        "CKP-REL-000009 Source Node "
        "CKP-TERM-000010 Relationship Type "
        "Used By Target Node CKP-TERM-000002"
    ) in content

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000008"
    ) in content


def test_all_relationships_use_canonical_types() -> None:
    content = ontology_text()

    for relationship_type in (
        "Is A",
        "Part Of",
        "Contains",
        "Tracked As",
        "Uses",
        "Used By",
        "Sold Through",
        "Applies To",
    ):
        assert relationship_type in content


def test_ontology_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Ontology Node shall reference one of "
        "the first ten registered Canonical Terms.",
        "Every Relationship Assertion shall reference "
        "registered Ontology Nodes.",
        "Every Relationship Assertion shall use a "
        "canonical Relationship Type.",
        "Every assertion shall declare directionality.",
        "Commerce shall remain the only root node.",
        "No duplicate semantic assertion shall exist.",
        "No frozen canonical definition shall be "
        "privately redefined.",
    ):
        assert constraint in content


def test_ontology_invariants_are_declared() -> None:
    content = ontology_text()

    for invariant in ONTOLOGY_INVARIANTS:
        assert invariant in content


def test_audit_evidence_requirements_are_declared() -> None:
    content = ontology_text()

    for evidence_type in (
        "Node Registration.",
        "Canonical Identity.",
        "Root Validation.",
        "Hierarchy Validation.",
        "Relationship Type Validation.",
        "Directionality Validation.",
        "Inverse Consistency.",
        "Duplicate Detection.",
        "Registry Closure.",
        "Semantic Closure.",
    ):
        assert evidence_type in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Exactly ten Ontology Nodes are declared.",
        "Commerce is the only root Ontology Node.",
        "Four hierarchy assertions are declared.",
        "Twelve canonical Relationship Assertions "
        "are declared.",
        "All assertions reference registered "
        "Ontology Nodes.",
        "All relationship types are canonical.",
        "Inverse-paired assertions are consistent.",
        "No duplicate assertion exists.",
        "Ontology invariants are declared.",
        "Audit Evidence requirements are declared.",
    ):
        assert criterion in content
