from dataclasses import FrozenInstanceError

import pytest

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


def test_graph_accepts_single_directly_observed_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    assert graph.total_rules == 1
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 0


def test_graph_accepts_derived_rule_with_existing_sources() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            direct("RULE-LYR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
                "RULE-LYR-001",
            ),
        ),
    )

    assert graph.total_rules == 3
    assert graph.directly_observed_count == 2
    assert graph.derived_count == 1


def test_graph_preserves_declared_record_order() -> None:
    records = (
        direct("RULE-LYR-001"),
        direct("RULE-CLR-001"),
    )

    graph = build_rule_provenance_graph(
        records=records,
    )

    assert tuple(
        record.rule_id
        for record in graph.records
    ) == (
        "RULE-LYR-001",
        "RULE-CLR-001",
    )


def test_graph_accepts_source_declared_after_dependent_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
            direct("RULE-CLR-001"),
        ),
    )

    assert graph.total_rules == 2
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 1


def test_graph_accepts_multilevel_derived_dependencies() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
            derived(
                "RULE-GEO-001",
                "RULE-PRD-003",
            ),
        ),
    )

    assert graph.total_rules == 3
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 2


def test_graph_rejects_mutable_record_collection() -> None:
    with pytest.raises(
        TypeError,
        match="records must be an immutable tuple",
    ):
        build_rule_provenance_graph(
            records=[
                direct("RULE-CLR-001"),
            ],
        )


def test_graph_rejects_empty_record_collection() -> None:
    with pytest.raises(
        ValueError,
        match="records must not be empty",
    ):
        build_rule_provenance_graph(
            records=(),
        )


def test_graph_rejects_invalid_record_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "every record must be a "
            "RetailContextRuleProvenance"
        ),
    ):
        build_rule_provenance_graph(
            records=(
                "RULE-CLR-001",
            ),
        )


def test_graph_rejects_duplicate_rule_identity() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate rule_id: RULE-CLR-001",
    ):
        build_rule_provenance_graph(
            records=(
                direct("RULE-CLR-001"),
                direct("RULE-CLR-001"),
            ),
        )


def test_graph_rejects_missing_dependency_source() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "missing source rule_id: "
            "RULE-CLR-001"
        ),
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "RULE-PRD-003",
                    "RULE-CLR-001",
                ),
            ),
        )


def test_graph_rejects_two_rule_cycle() -> None:
    with pytest.raises(
        ValueError,
        match="cyclic rule dependency detected",
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "RULE-PRD-003",
                    "RULE-GEO-001",
                ),
                derived(
                    "RULE-GEO-001",
                    "RULE-PRD-003",
                ),
            ),
        )


def test_graph_rejects_three_rule_cycle() -> None:
    with pytest.raises(
        ValueError,
        match="cyclic rule dependency detected",
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "RULE-PRD-003",
                    "RULE-GEO-001",
                ),
                derived(
                    "RULE-GEO-001",
                    "RULE-LYR-003",
                ),
                derived(
                    "RULE-LYR-003",
                    "RULE-PRD-003",
                ),
            ),
        )


def test_graph_accepts_shared_direct_source() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
            derived(
                "RULE-GEO-001",
                "RULE-CLR-001",
            ),
        ),
    )

    assert graph.directly_observed_count == 1
    assert graph.derived_count == 2


def test_graph_accepts_converging_acyclic_dependencies() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
            derived(
                "RULE-LYR-003",
                "RULE-CLR-001",
            ),
            derived(
                "RULE-GEO-001",
                "RULE-PRD-003",
                "RULE-LYR-003",
            ),
        ),
    )

    assert graph.total_rules == 4
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 3


def test_graph_result_is_immutable() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        graph.total_rules = 2


def test_graph_records_are_immutable() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
        ),
    )

    with pytest.raises(TypeError):
        graph.records[0] = direct(
            "RULE-CLR-002"
        )


def test_graph_does_not_claim_operational_independence() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("RULE-CLR-001"),
            derived(
                "RULE-PRD-003",
                "RULE-CLR-001",
            ),
        ),
    )

    assert not hasattr(
        graph,
        "independent_interventions",
    )

    assert not hasattr(
        graph,
        "commercial_revenue",
    )

    assert not hasattr(
        graph,
        "customer_accepted",
    )
