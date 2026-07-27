import re
from pathlib import Path


QUERIES = Path(
    "research/commerce/query_language/initial/"
    "INITIAL_EXECUTABLE_QUERIES.md"
)

GRAPH = Path(
    "research/commerce/knowledge_graph/initial/"
    "INITIAL_COMMERCE_KNOWLEDGE_GRAPH.md"
)

EXPECTED_QUERY_IDS = tuple(
    f"CKP-QUERY-{number:06d}"
    for number in range(1, 21)
)

EXPECTED_NODE_IDS = tuple(
    f"CKP-TERM-{number:06d}"
    for number in range(1, 11)
)

EXPECTED_EDGE_IDS = tuple(
    f"CKP-REL-{number:06d}"
    for number in range(1, 13)
)

EXPECTED_PATH_IDS = tuple(
    f"CKP-PATH-{number:06d}"
    for number in range(1, 5)
)

QUERY_FORMS = (
    "SELECT NODE",
    "SELECT EDGE",
    "SELECT PATH",
    "VALIDATE EXISTS",
    "VALIDATE RELATIONSHIP",
    "VALIDATE REACHABLE",
    "VALIDATE PATH",
)

INVARIANTS = (
    "Read-Only Preservation.",
    "Canonical Query Identity.",
    "Immutable Graph Target.",
    "Query Form Canonicality.",
    "Selection Target Compatibility.",
    "Selection Cardinality Integrity.",
    "Filter Property Canonicality.",
    "Filter Operator Validity.",
    "Filter Value Compatibility.",
    "Filter Group Closure.",
    "Deterministic Filter Ordering.",
    "Projection Property Canonicality.",
    "Deterministic Projection Position.",
    "Deterministic Result Ordering.",
    "Pagination Boundary Integrity.",
    "Matched Record Count Preservation.",
    "Returned Record Count Integrity.",
    "Canonical Validation Type.",
    "Expected Result Independence.",
    "Validation Outcome Integrity.",
    "Expectation Match Integrity.",
    "Direct Relationship Semantics.",
    "Reachability Maximum Depth Enforcement.",
    "Witness Path Continuity.",
    "Registered Path Closure.",
    "Composed Path Non-Registration.",
    "No Implicit Edges.",
    "Vocabulary Compatibility.",
    "Ontology Compatibility.",
    "Graph Compatibility.",
    "Query Evidence Completeness.",
    "Query Integrity.",
    "Result Integrity.",
    "Canonical Serialization.",
    "Deterministic Execution Specification.",
    "Fail-Closed Validation.",
    "Semantic Closure.",
    "Traceability Closure.",
)


def query_text() -> str:
    return QUERIES.read_text(
        encoding="utf-8",
    )


def normalized_text() -> str:
    return " ".join(
        query_text().split()
    )


def graph_text() -> str:
    return GRAPH.read_text(
        encoding="utf-8",
    )


def query_block(number: int) -> str:
    identifier = f"IEQ-{number:03d}"

    pattern = (
        rf"^## {re.escape(identifier)} — [^\n]*$"
        rf"(.*?)(?=^## IEQ-\d{{3}} — |"
        rf"^## Deterministic Query Order$)"
    )

    match = re.search(
        pattern,
        query_text(),
        flags=re.MULTILINE | re.DOTALL,
    )

    assert match is not None, (
        f"missing executable query {identifier}"
    )

    return " ".join(
        match.group(1).split()
    )


def graph_node_ids() -> set[str]:
    return set(
        re.findall(
            r"^### (CKP-TERM-\d{6})$",
            graph_text(),
            flags=re.MULTILINE,
        )
    )


def graph_edge_ids() -> set[str]:
    return set(
        re.findall(
            r"^### (CKP-REL-\d{6})$",
            graph_text(),
            flags=re.MULTILINE,
        )
    )


def graph_path_ids() -> set[str]:
    return set(
        re.findall(
            r"^### (CKP-PATH-\d{6})$",
            graph_text(),
            flags=re.MULTILINE,
        )
    )


def test_initial_executable_queries_exist() -> None:
    assert QUERIES.is_file()


def test_initial_graph_exists() -> None:
    assert GRAPH.is_file()


def test_execution_boundary_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-GRAPH-000001",
        "Graph Version 1.0",
        "10 registered Graph Nodes.",
        "12 registered Graph Edges.",
        "4 registered Graph Paths.",
        "CKP-001 Canonical Commerce Vocabulary 1.0.",
        "CKP-002 Commerce Ontology 1.0.",
        "CKP-003 Commerce Knowledge Graph 1.0.",
    ):
        assert requirement in content


def test_execution_context_is_declared() -> None:
    content = normalized_text()

    for requirement in (
        "CKP-QUERY-CONTEXT-000001",
        "Maximum Result Limit 100",
        "Maximum Validation Depth 10",
        "The Initial Execution Context is immutable.",
    ):
        assert requirement in content


def test_exactly_twenty_queries_are_declared() -> None:
    headings = re.findall(
        r"^## IEQ-\d{3} — .+$",
        query_text(),
        flags=re.MULTILINE,
    )

    assert len(headings) == 20
    assert len(set(headings)) == 20


def test_query_identifiers_are_complete_and_unique() -> None:
    blocks = tuple(
        query_block(number)
        for number in range(1, 21)
    )

    found = []

    for block in blocks:
        match = re.search(
            r"Query Identifier (CKP-QUERY-\d{6})",
            block,
        )

        assert match is not None
        found.append(match.group(1))

    assert tuple(found) == EXPECTED_QUERY_IDS
    assert len(set(found)) == 20


def test_query_forms_are_represented() -> None:
    content = normalized_text()

    for query_form in QUERY_FORMS:
        assert query_form in content


def test_query_counts_are_declared() -> None:
    content = normalized_text()

    for count in (
        "Initial Executable Query Count 20",
        "SELECT NODE Query Count 4",
        "SELECT EDGE Query Count 4",
        "SELECT PATH Query Count 2",
        "VALIDATE EXISTS Query Count 2",
        "VALIDATE RELATIONSHIP Query Count 3",
        "VALIDATE REACHABLE Query Count 2",
        "VALIDATE PATH Query Count 3",
    ):
        assert count in content


def test_select_all_nodes_matches_graph_registry() -> None:
    block = query_block(1)

    assert set(EXPECTED_NODE_IDS).issubset(
        set(re.findall(r"CKP-TERM-\d{6}", block))
    )

    assert "Expected Matched Record Count 10" in block
    assert "Expected Returned Record Count 10" in block

    assert graph_node_ids() == set(EXPECTED_NODE_IDS)


def test_select_retail_node_is_exact() -> None:
    block = query_block(2)

    for requirement in (
        "Filter Property Canonical Identifier",
        "Filter Operator EQUALS",
        "Filter Value CKP-TERM-000002",
        "Expected Preferred Name Retail",
        "Expected Matched Record Count 1",
        "Expected Returned Record Count 1",
    ):
        assert requirement in block


def test_commerce_model_selection_is_deterministic() -> None:
    block = query_block(3)

    expected = {
        "CKP-TERM-000002",
        "CKP-TERM-000003",
        "CKP-TERM-000005",
    }

    matched = set(
        re.findall(
            r"CKP-TERM-\d{6}",
            block.split(
                "Expected Matched Identifiers",
                maxsplit=1,
            )[1],
        )
    )

    assert expected.issubset(matched)
    assert "Expected Matched Record Count 3" in block


def test_is_a_edge_selection_matches_graph() -> None:
    block = query_block(4)

    expected = {
        "CKP-REL-000001",
        "CKP-REL-000002",
        "CKP-REL-000003",
        "CKP-REL-000004",
    }

    assert expected.issubset(
        set(re.findall(r"CKP-REL-\d{6}", block))
    )

    assert "Expected Matched Record Count 4" in block


def test_product_semantic_edge_query_uses_explicit_or_group() -> None:
    block = query_block(6)

    for requirement in (
        "CKP-FILTER-GROUP-000006",
        "Group Conjunction OR",
        "CKP-FILTER-000006-A",
        "CKP-FILTER-000006-B",
        "Filter Priority 0",
        "Filter Priority 1",
    ):
        assert requirement in block

    expected = {
        "CKP-REL-000005",
        "CKP-REL-000006",
        "CKP-REL-000007",
        "CKP-REL-000010",
    }

    assert expected.issubset(
        set(re.findall(r"CKP-REL-\d{6}", block))
    )


def test_registered_path_selection_matches_graph() -> None:
    block = query_block(7)

    assert set(EXPECTED_PATH_IDS).issubset(
        set(re.findall(r"CKP-PATH-\d{6}", block))
    )

    assert graph_path_ids() == set(EXPECTED_PATH_IDS)
    assert "Expected Matched Record Count 4" in block


def test_path_length_filter_selects_composite_path() -> None:
    block = query_block(8)

    for requirement in (
        "Filter Property Path Length",
        "Filter Operator GREATER THAN",
        "Filter Value Type INTEGER",
        "Filter Value 1",
        "CKP-PATH-000004",
        "Expected Matched Record Count 1",
    ):
        assert requirement in block


def test_node_pagination_boundary_is_deterministic() -> None:
    block = query_block(9)

    for requirement in (
        "Limit 3.",
        "Offset 2.",
        "CKP-TERM-000003.",
        "CKP-TERM-000004.",
        "CKP-TERM-000005.",
        "Expected Matched Record Count 10",
        "Expected Returned Record Count 3",
        "Expected Offset 2",
        "Expected Limit 3",
    ):
        assert requirement in block


def test_exists_positive_query_is_defined() -> None:
    block = query_block(10)

    for requirement in (
        "Validation Type EXISTS",
        "Subject Identifier CKP-TERM-000002",
        "Expected Result TRUE",
        "Expected Validation Outcome TRUE",
        "Expected Expectation Match Result MATCH",
    ):
        assert requirement in block


def test_exists_negative_query_returns_false_not_error() -> None:
    block = query_block(11)

    for requirement in (
        "Subject Identifier CKP-TERM-999999",
        "Expected Result FALSE",
        "Expected Validation Outcome FALSE",
        "Expected Expectation Match Result MATCH",
        "Expected Validation Status Completed",
    ):
        assert requirement in block


def test_direct_relationship_positive_query_is_defined() -> None:
    block = query_block(12)

    for requirement in (
        "Subject Identifier CKP-TERM-000002",
        "Object Identifier CKP-TERM-000001",
        "Canonical Relationship Type Is A",
        "Validation Direction FORWARD",
        "CKP-REL-000001.",
        "Expected Validation Outcome TRUE",
    ):
        assert requirement in block


def test_direct_relationship_negative_query_preserves_direction() -> None:
    block = query_block(13)

    for requirement in (
        "Subject Identifier CKP-TERM-000001",
        "Object Identifier CKP-TERM-000002",
        "Canonical Relationship Type Is A",
        "Validation Direction FORWARD",
        "Expected Validation Outcome FALSE",
        "Expected Expectation Match Result MATCH",
    ):
        assert requirement in block


def test_inverse_semantic_relationship_query_is_defined() -> None:
    block = query_block(14)

    for requirement in (
        "Subject Identifier CKP-TERM-000006",
        "Object Identifier CKP-TERM-000007",
        "Canonical Relationship Type Contains",
        "CKP-REL-000006.",
        "Expected Validation Outcome TRUE",
    ):
        assert requirement in block


def test_reachability_positive_query_uses_registered_witness() -> None:
    block = query_block(15)

    for requirement in (
        "Subject Identifier CKP-TERM-000008",
        "Object Identifier CKP-TERM-000006",
        "Traversal Strategy SEMANTIC",
        "Maximum Depth 2",
        "CKP-PATH-000004",
        "CKP-REL-000011.",
        "CKP-REL-000005.",
        "Expected Path Length 2",
        "Expected Validation Outcome TRUE",
    ):
        assert requirement in block


def test_reachability_depth_boundary_returns_false() -> None:
    block = query_block(16)

    for requirement in (
        "Maximum Depth 1",
        "Expected Result FALSE",
        "Expected Validation Outcome FALSE",
        "Expected Witness Path Identifier None",
        "Expected Validation Status Completed",
    ):
        assert requirement in block


def test_registered_path_validation_is_defined() -> None:
    block = query_block(17)

    for requirement in (
        "Path Validation Mode REGISTERED PATH",
        "Path Identifier CKP-PATH-000004",
        "Expected Path Length 2",
        "Expected Path Continuity Result Valid",
        "Expected Validation Outcome TRUE",
    ):
        assert requirement in block


def test_composed_path_validation_does_not_register() -> None:
    block = query_block(18)

    for requirement in (
        "Path Validation Mode COMPOSED PATH",
        "CKP-TERM-000006.",
        "CKP-TERM-000010.",
        "CKP-REL-000010.",
        "Declared Path Length 1",
        "Expected Registration Effect None",
        "Expected Validation Outcome TRUE",
    ):
        assert requirement in block


def test_disconnected_path_fails_closed() -> None:
    block = query_block(19)

    for requirement in (
        "Expected Validation Outcome ERROR",
        "Expected Expectation Match Result NOT EVALUATED",
        "Expected Path Continuity Result Invalid",
        "Expected Failure Classification PATH_CONTINUITY_VIOLATION",
        "Expected Validation Status Failed",
    ):
        assert requirement in block


def test_edge_pagination_returns_first_two_edges() -> None:
    block = query_block(20)

    for requirement in (
        "Expected Matched Record Count 12",
        "CKP-REL-000001.",
        "CKP-REL-000002.",
        "Expected Returned Record Count 2",
    ):
        assert requirement in block


def test_expected_graph_components_are_registered() -> None:
    assert set(EXPECTED_NODE_IDS) == graph_node_ids()
    assert set(EXPECTED_EDGE_IDS) == graph_edge_ids()
    assert set(EXPECTED_PATH_IDS) == graph_path_ids()


def test_evidence_is_required_for_every_outcome() -> None:
    content = normalized_text()

    assert (
        "No successful, false, failed, or cancelled "
        "query shall omit evidence."
    ) in content

    for number in range(1, 21):
        block = query_block(number)

        assert (
            f"CKP-QUERY-EVIDENCE-{number:06d}"
            in block
        )


def test_result_integrity_is_required_for_every_query() -> None:
    for number in range(1, 21):
        block = query_block(number)

        assert (
            f"CKP-QUERY-RESULT-INTEGRITY-{number:06d}"
            in block
        )


def test_deterministic_query_order_is_complete() -> None:
    section = query_text().split(
        "## Deterministic Query Order",
        maxsplit=1,
    )[1].split(
        "## Query Count",
        maxsplit=1,
    )[0]

    found = tuple(
        re.findall(
            r"CKP-QUERY-\d{6}",
            section,
        )
    )

    assert found == EXPECTED_QUERY_IDS


def test_failure_behavior_distinguishes_false_and_error() -> None:
    content = normalized_text()

    for rule in (
        "A structurally valid negative proposition "
        "shall return FALSE rather than ERROR.",
        "An unevaluable proposition shall return ERROR.",
        "FALSE shall remain a valid Validation Outcome.",
        "ERROR shall not be converted into FALSE.",
    ):
        assert rule in content


def test_read_only_boundary_is_declared() -> None:
    content = normalized_text()

    for prohibition in (
        "Create a Graph Node.",
        "Create a Graph Edge.",
        "Create a Graph Path.",
        "Register a composed Graph Path.",
        "Delete a Graph Node.",
        "Delete a Graph Edge.",
        "Delete a Graph Path.",
        "Modify a Graph Component.",
        "Repair a broken relationship.",
        "Repair a disconnected path.",
        "Modify CKP-001.",
        "Modify CKP-002.",
        "Modify CKP-003.",
        "Create undocumented semantic meaning.",
    ):
        assert prohibition in content


def test_invariants_are_declared() -> None:
    content = normalized_text()

    for invariant in INVARIANTS:
        assert invariant in content


def test_release_criteria_are_declared() -> None:
    content = normalized_text()

    for criterion in (
        "Execution Boundary is explicitly defined.",
        "Executable Query Contract is explicitly defined.",
        "Execution Context is explicitly defined.",
        "Canonical Result Ordering is explicitly defined.",
        "SELECT NODE queries are declared.",
        "SELECT EDGE queries are declared.",
        "SELECT PATH queries are declared.",
        "VALIDATE EXISTS queries are declared.",
        "VALIDATE RELATIONSHIP queries are declared.",
        "VALIDATE REACHABLE queries are declared.",
        "VALIDATE PATH queries are declared.",
        "Positive validation outcomes are declared.",
        "Negative validation outcomes are declared.",
        "Error validation outcomes are declared.",
        "Deterministic pagination is demonstrated.",
        "Deterministic witness path selection is demonstrated.",
        "Exactly twenty Initial Executable Queries are declared.",
        "Read-Only Boundary is declared.",
        "Executable Query Invariants are declared.",
    ):
        assert criterion in content


def test_next_deliverable_is_declared() -> None:
    content = normalized_text()

    assert "CKP-004.9" in content
    assert "Query Consistency Audit." in content
