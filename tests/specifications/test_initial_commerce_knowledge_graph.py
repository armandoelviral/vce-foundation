import re
from pathlib import Path


GRAPH = Path(
    "research/commerce/knowledge_graph/initial/"
    "INITIAL_COMMERCE_KNOWLEDGE_GRAPH.md"
)

TERM_DIRECTORY = Path(
    "research/commerce/registry/terms"
)

ONTOLOGY = Path(
    "research/commerce/ontology/"
    "INITIAL_COMMERCE_ONTOLOGY.md"
)

EXPECTED_NODES = {
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

EXPECTED_EDGES = {
    "CKP-REL-000001": (
        "CKP-TERM-000002",
        "Is A",
        "CKP-TERM-000001",
    ),
    "CKP-REL-000002": (
        "CKP-TERM-000003",
        "Is A",
        "CKP-TERM-000001",
    ),
    "CKP-REL-000003": (
        "CKP-TERM-000004",
        "Is A",
        "CKP-TERM-000001",
    ),
    "CKP-REL-000004": (
        "CKP-TERM-000005",
        "Is A",
        "CKP-TERM-000001",
    ),
    "CKP-REL-000005": (
        "CKP-TERM-000007",
        "Part Of",
        "CKP-TERM-000006",
    ),
    "CKP-REL-000006": (
        "CKP-TERM-000006",
        "Contains",
        "CKP-TERM-000007",
    ),
    "CKP-REL-000007": (
        "CKP-TERM-000006",
        "Tracked As",
        "CKP-TERM-000007",
    ),
    "CKP-REL-000008": (
        "CKP-TERM-000002",
        "Uses",
        "CKP-TERM-000010",
    ),
    "CKP-REL-000009": (
        "CKP-TERM-000010",
        "Used By",
        "CKP-TERM-000002",
    ),
    "CKP-REL-000010": (
        "CKP-TERM-000006",
        "Sold Through",
        "CKP-TERM-000010",
    ),
    "CKP-REL-000011": (
        "CKP-TERM-000008",
        "Applies To",
        "CKP-TERM-000007",
    ),
    "CKP-REL-000012": (
        "CKP-TERM-000009",
        "Uses",
        "CKP-TERM-000010",
    ),
}

GRAPH_INVARIANTS = (
    "Canonical Identity Preservation.",
    "Registered Node Closure.",
    "Canonical Edge Closure.",
    "Single Root Preservation.",
    "Direction Preservation.",
    "Inverse Relationship Consistency.",
    "Hierarchy Acyclicity.",
    "No Duplicate Nodes.",
    "No Duplicate Edges.",
    "No Orphan Nodes.",
    "No Orphan Edges.",
    "No Implicit Edges.",
    "No Initial Reflexivity.",
    "Path Continuity.",
    "Deterministic Node Ordering.",
    "Deterministic Edge Ordering.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Semantic Closure.",
    "Traceability Closure.",
    "Graph Evidence Completeness.",
)


def graph_text() -> str:
    return GRAPH.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        graph_text().split()
    )


def registered_term_ids() -> set[str]:
    return {
        path.name.split("_", maxsplit=1)[0]
        for path in TERM_DIRECTORY.glob(
            "CKP-TERM-*.md"
        )
    }


def ontology_relationship_ids() -> set[str]:
    return set(
        re.findall(
            r"CKP-REL-\d{6}",
            ONTOLOGY.read_text(
                encoding="utf-8",
            ),
        )
    )


def graph_node_ids() -> tuple[str, ...]:
    graph_nodes_section = graph_text().split(
        "## Graph Nodes",
        maxsplit=1,
    )[1].split(
        "## Hierarchy Graph Edges",
        maxsplit=1,
    )[0]

    return tuple(
        re.findall(
            r"^### (CKP-TERM-\d{6})$",
            graph_nodes_section,
            flags=re.MULTILINE,
        )
    )


def graph_edge_ids() -> tuple[str, ...]:
    edge_section = graph_text().split(
        "## Hierarchy Graph Edges",
        maxsplit=1,
    )[1].split(
        "## Deterministic Node Order",
        maxsplit=1,
    )[0]

    return tuple(
        re.findall(
            r"^### (CKP-REL-\d{6})$",
            edge_section,
            flags=re.MULTILINE,
        )
    )


def edge_block(identifier: str) -> str:
    pattern = (
        rf"^### {re.escape(identifier)}$"
        rf"(.*?)(?=^### CKP-REL-\d{{6}}$|"
        rf"^## Deterministic Node Order$)"
    )

    match = re.search(
        pattern,
        graph_text(),
        flags=re.MULTILINE | re.DOTALL,
    )

    assert match is not None, (
        f"missing edge block {identifier}"
    )

    return " ".join(
        match.group(1).split()
    )


def test_initial_graph_exists() -> None:
    assert GRAPH.is_file()


def test_graph_manifest_is_declared() -> None:
    content = normalized_text()

    for item in (
        "Graph Identifier CKP-GRAPH-000001",
        "Graph Version 1.0",
        "Root Node Identifier CKP-TERM-000001",
        "Node Count 10",
        "Edge Count 12",
        "CKP-GRAPH-INTEGRITY-000001",
    ):
        assert item in content


def test_frozen_baselines_are_declared() -> None:
    content = graph_text()

    assert (
        "CKP-001 Canonical Commerce Vocabulary 1.0"
        in content
    )

    assert (
        "CKP-002 Commerce Ontology 1.0"
        in content
    )


def test_exactly_ten_graph_nodes_are_declared() -> None:
    node_ids = graph_node_ids()

    assert len(node_ids) == 10
    assert len(set(node_ids)) == 10


def test_graph_nodes_equal_registered_terms() -> None:
    assert set(graph_node_ids()) == (
        registered_term_ids()
    )


def test_all_expected_nodes_are_declared() -> None:
    content = graph_text()

    for identifier, preferred_name in (
        EXPECTED_NODES.items()
    ):
        assert identifier in content
        assert preferred_name in content


def test_every_graph_node_is_a_term() -> None:
    graph_nodes_section = graph_text().split(
        "## Graph Nodes",
        maxsplit=1,
    )[1].split(
        "## Hierarchy Graph Edges",
        maxsplit=1,
    )[0]

    assert (
        graph_nodes_section.count(
            "Knowledge Object Type\n\nTERM"
        )
        == 10
    )


def test_commerce_is_the_only_root() -> None:
    content = normalized_text()

    assert (
        "Root Node Identifier CKP-TERM-000001"
        in content
    )

    assert (
        "Commerce is the only root Graph Node."
        in content
    )

    assert (
        "Exactly one root Graph Node is declared."
        in content
    )


def test_exactly_twelve_graph_edges_are_declared() -> None:
    edge_ids = graph_edge_ids()

    assert len(edge_ids) == 12
    assert len(set(edge_ids)) == 12


def test_graph_edges_equal_frozen_ontology_assertions() -> None:
    assert set(graph_edge_ids()) == (
        ontology_relationship_ids()
    )


def test_every_edge_has_expected_semantics() -> None:
    for identifier, (
        source,
        relationship_type,
        target,
    ) in EXPECTED_EDGES.items():
        block = edge_block(identifier)

        assert (
            f"Source Node Identifier {source}"
            in block
        )

        assert (
            "Canonical Relationship Type "
            f"{relationship_type}"
            in block
        )

        assert (
            f"Target Node Identifier {target}"
            in block
        )

        assert (
            "Ontology Assertion Reference "
            f"{identifier}"
            in block
        )


def test_four_hierarchy_edges_are_declared() -> None:
    content = normalized_text()

    hierarchy_assertions = (
        "Retail Is A Commerce.",
        "Wholesale Is A Commerce.",
        "Ecommerce Is A Commerce.",
        "Informal Commerce Is A Commerce.",
    )

    for assertion in hierarchy_assertions:
        assert assertion in content


def test_eight_semantic_edges_are_declared() -> None:
    content = normalized_text()

    semantic_assertions = (
        "SKU Part Of Product.",
        "Product Contains SKU.",
        "Product Tracked As SKU.",
        "Retail Uses Channel.",
        "Channel Used By Retail.",
        "Product Sold Through Channel.",
        "Inventory Applies To SKU.",
        "Customer Uses Channel.",
    )

    for assertion in semantic_assertions:
        assert assertion in content


def test_part_of_contains_inverse_pair_is_consistent() -> None:
    part_of = edge_block(
        "CKP-REL-000005"
    )
    contains = edge_block(
        "CKP-REL-000006"
    )

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000006"
        in part_of
    )

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000005"
        in contains
    )


def test_uses_used_by_inverse_pair_is_consistent() -> None:
    uses = edge_block(
        "CKP-REL-000008"
    )
    used_by = edge_block(
        "CKP-REL-000009"
    )

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000009"
        in uses
    )

    assert (
        "Inverse Relationship Reference "
        "CKP-REL-000008"
        in used_by
    )


def test_unidirectional_edges_declare_no_inverse() -> None:
    for identifier in (
        "CKP-REL-000001",
        "CKP-REL-000002",
        "CKP-REL-000003",
        "CKP-REL-000004",
        "CKP-REL-000007",
        "CKP-REL-000010",
        "CKP-REL-000011",
        "CKP-REL-000012",
    ):
        block = edge_block(identifier)

        assert (
            "Directionality Unidirectional"
            in block
        )

        assert (
            "Inverse Relationship Reference None"
            in block
        )


def test_no_graph_edge_is_reflexive() -> None:
    for identifier, (
        source,
        _relationship_type,
        target,
    ) in EXPECTED_EDGES.items():
        assert source != target, identifier


def test_node_order_is_deterministic() -> None:
    section = graph_text().split(
        "## Deterministic Node Order",
        maxsplit=1,
    )[1].split(
        "## Deterministic Edge Order",
        maxsplit=1,
    )[0]

    ordered_ids = re.findall(
        r"CKP-TERM-\d{6}",
        section,
    )

    assert ordered_ids == sorted(
        EXPECTED_NODES
    )


def test_edge_order_is_deterministic() -> None:
    section = graph_text().split(
        "## Deterministic Edge Order",
        maxsplit=1,
    )[1].split(
        "## Registered Direct Paths",
        maxsplit=1,
    )[0]

    ordered_ids = re.findall(
        r"CKP-REL-\d{6}",
        section,
    )

    assert ordered_ids == sorted(
        EXPECTED_EDGES
    )


def test_registered_paths_are_declared() -> None:
    content = graph_text()

    for identifier in (
        "CKP-PATH-000001",
        "CKP-PATH-000002",
        "CKP-PATH-000003",
        "CKP-PATH-000004",
    ):
        assert identifier in content


def test_composite_path_is_continuous() -> None:
    content = normalized_text()

    assert (
        "CKP-PATH-000004 Start Node Identifier "
        "CKP-TERM-000008"
        in content
    )

    assert (
        "Ordered Node Sequence CKP-TERM-000008 "
        "CKP-TERM-000007 CKP-TERM-000006"
        in content
    )

    assert (
        "Ordered Edge Sequence CKP-REL-000011 "
        "CKP-REL-000005"
        in content
    )

    assert "Path Length 2" in content
    assert "Path Continuity Valid" in content


def test_graph_constraints_are_declared() -> None:
    content = normalized_text()

    for constraint in (
        "Every Graph Node shall reference one "
        "registered Canonical Commerce Term.",
        "Every Graph Edge shall reference registered "
        "Source and Target Graph Nodes.",
        "Every Graph Edge shall derive from one frozen "
        "CKP-002 Ontology Assertion.",
        "Commerce shall remain the only root Graph Node.",
        "No duplicate Graph Node shall exist.",
        "No duplicate Graph Edge shall exist.",
        "No orphan Graph Node shall exist.",
        "No orphan Graph Edge shall exist.",
        "No implicit Graph Edge shall exist.",
        "No initial Graph Edge shall be reflexive.",
    ):
        assert constraint in content


def test_graph_invariants_are_declared() -> None:
    content = graph_text()

    for invariant in GRAPH_INVARIANTS:
        assert invariant in content


def test_graph_validation_evidence_is_declared() -> None:
    content = graph_text()

    for evidence_type in (
        "Graph Manifest Validation.",
        "Node Count Validation.",
        "Edge Count Validation.",
        "Root Node Validation.",
        "Node Registry Closure.",
        "Edge Ontology Closure.",
        "Directionality Validation.",
        "Inverse Relationship Validation.",
        "Hierarchy Acyclicity Validation.",
        "Path Continuity Validation.",
        "Deterministic Ordering Validation.",
        "Graph Integrity Validation.",
    ):
        assert evidence_type in content


def test_graph_integrity_is_declared() -> None:
    content = normalized_text()

    assert (
        "Graph Integrity Reference "
        "CKP-GRAPH-INTEGRITY-000001"
        in content
    )

    for bound_property in (
        "Graph Identifier.",
        "Graph Version.",
        "Root Node Identifier.",
        "Deterministic Node Order.",
        "Deterministic Edge Order.",
        "Vocabulary Baseline.",
        "Ontology Baseline.",
        "Node Count.",
        "Edge Count.",
    ):
        assert bound_property in graph_text()


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "One Graph Manifest is declared.",
        "Graph Identifier CKP-GRAPH-000001 is declared.",
        "Exactly ten Graph Nodes are declared.",
        "Exactly twelve Graph Edges are declared.",
        "Exactly one root Graph Node is declared.",
        "CKP-TERM-000001 is the root Graph Node.",
        "Four hierarchy Graph Edges are declared.",
        "Eight semantic Graph Edges are declared.",
        "Canonical directionality is preserved.",
        "Inverse-paired Graph Edges are consistent.",
        "Deterministic Node Order is declared.",
        "Deterministic Edge Order is declared.",
        "Registered Graph Paths are declared.",
        "Path Continuity is demonstrated.",
        "Graph Constraints are declared.",
        "Graph Invariants are declared.",
        "Graph Validation Evidence is declared.",
        "Graph Integrity is declared.",
    ):
        assert criterion in content
