from dataclasses import FrozenInstanceError

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
    RetailContextDependencySource,
)
from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
    RuleProvenanceType,
)
from sp001.contracts.retail_context_rule_provenance_graph import (
    build_rule_provenance_graph,
)


def direct(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )


def derived(
    rule_id: str,
    *source_rule_ids: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=source_rule_ids,
    )


def assessed(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.EVIDENCE_ASSESSED
        ),
    )


def test_graph_exposes_evidence_assessed_count() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("GEO-004"),
        ),
    )

    assert graph.evidence_assessed_count == 1


def test_graph_counts_single_evidence_assessed_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("PHO-002"),
        ),
    )

    assert graph.total_rules == 1
    assert graph.directly_observed_count == 0
    assert graph.derived_count == 0
    assert graph.evidence_assessed_count == 1


def test_graph_preserves_zero_assessed_count_for_direct_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
        ),
    )

    assert graph.total_rules == 1
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 0
    assert graph.evidence_assessed_count == 0


def test_graph_preserves_zero_assessed_count_for_derived_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            derived(
                "GEO-001",
                "CLR-001",
            ),
        ),
    )

    assert graph.total_rules == 2
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 1
    assert graph.evidence_assessed_count == 0


def test_graph_counts_multiple_evidence_assessed_rules() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("GEO-004"),
            assessed("PHO-002"),
            assessed("CAP-001"),
        ),
    )

    assert graph.total_rules == 3
    assert graph.evidence_assessed_count == 3


def test_graph_separates_assessed_and_directly_observed_rules() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            assessed("GEO-004"),
        ),
    )

    assert graph.directly_observed_count == 1
    assert graph.evidence_assessed_count == 1


def test_graph_separates_assessed_and_derived_rules() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            derived(
                "GEO-001",
                "CLR-001",
            ),
            assessed("GEO-004"),
        ),
    )

    assert graph.derived_count == 1
    assert graph.evidence_assessed_count == 1


def test_graph_reconciles_three_provenance_categories() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            direct("CLR-002"),
            derived(
                "GEO-001",
                "CLR-001",
                "CLR-002",
            ),
            assessed("GEO-004"),
            assessed("PHO-002"),
        ),
    )

    assert (
        graph.directly_observed_count
        + graph.derived_count
        + graph.evidence_assessed_count
    ) == graph.total_rules

    assert graph.total_rules == 5


def test_graph_represents_five_canonical_evidence_limited_rules() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("GEO-004"),
            assessed("PHO-002"),
            assessed("CAP-001"),
            assessed("CAP-003"),
            assessed("CAP-004"),
        ),
    )

    assert graph.total_rules == 5
    assert graph.evidence_assessed_count == 5
    assert graph.directly_observed_count == 0
    assert graph.derived_count == 0


def test_graph_keeps_context_policy_outside_provenance_counts() -> None:
    policy = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=(
            DependencySourceType.CONTEXT_POLICY
        ),
    )

    adapted_fixture = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        dependency_sources=(
            policy,
        ),
    )

    graph = build_rule_provenance_graph(
        records=(
            adapted_fixture,
            assessed("CAP-004"),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert graph.total_rules == 2
    assert graph.derived_count == 1
    assert graph.evidence_assessed_count == 1

    assert graph.context_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
    )


def test_assessed_rule_does_not_become_direct_evidence() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("CAP-003"),
        ),
    )

    assert graph.directly_observed_count == 0


def test_assessed_rule_does_not_become_derived_evidence() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("CAP-004"),
        ),
    )

    assert graph.derived_count == 0


def test_assessed_count_preserves_declared_record_order() -> None:
    records = (
        assessed("CAP-004"),
        direct("CLR-001"),
        assessed("GEO-004"),
    )

    graph = build_rule_provenance_graph(
        records=records,
    )

    assert tuple(
        record.rule_id
        for record in graph.records
    ) == (
        "CAP-004",
        "CLR-001",
        "GEO-004",
    )

    assert graph.evidence_assessed_count == 2


def test_evidence_assessed_count_is_immutable() -> None:
    graph = build_rule_provenance_graph(
        records=(
            assessed("GEO-004"),
        ),
    )

    try:
        graph.evidence_assessed_count = 0
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError(
            "evidence_assessed_count must remain immutable"
        )
