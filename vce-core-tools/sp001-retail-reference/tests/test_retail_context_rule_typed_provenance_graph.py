from dataclasses import FrozenInstanceError

import pytest

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


def rule_source(
    source_id: str,
) -> RetailContextDependencySource:
    return RetailContextDependencySource(
        source_id=source_id,
        source_type=DependencySourceType.RULE,
    )


def policy_source(
    source_id: str,
) -> RetailContextDependencySource:
    return RetailContextDependencySource(
        source_id=source_id,
        source_type=(
            DependencySourceType.CONTEXT_POLICY
        ),
    )


def derived(
    rule_id: str,
    *,
    source_rule_ids: tuple[str, ...] = (),
    dependency_sources: tuple[
        RetailContextDependencySource,
        ...,
    ] = (),
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=source_rule_ids,
        dependency_sources=dependency_sources,
    )


def test_legacy_graph_defaults_to_no_context_policies() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
        ),
    )

    assert graph.context_policy_ids == ()
    assert graph.total_rules == 1


def test_graph_accepts_typed_rule_source() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            derived(
                "GEO-001",
                dependency_sources=(
                    rule_source("CLR-001"),
                ),
            ),
        ),
    )

    assert graph.total_rules == 2
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 1


def test_graph_accepts_typed_rule_declared_after_dependent() -> None:
    graph = build_rule_provenance_graph(
        records=(
            derived(
                "GEO-001",
                dependency_sources=(
                    rule_source("CLR-001"),
                ),
            ),
            direct("CLR-001"),
        ),
    )

    assert graph.total_rules == 2


def test_graph_rejects_missing_typed_rule_source() -> None:
    with pytest.raises(
        ValueError,
        match="missing source rule_id: CLR-001",
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "GEO-001",
                    dependency_sources=(
                        rule_source("CLR-001"),
                    ),
                ),
            ),
        )


def test_graph_detects_cycle_between_typed_rule_sources() -> None:
    with pytest.raises(
        ValueError,
        match="cyclic rule dependency detected",
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "GEO-001",
                    dependency_sources=(
                        rule_source("PRD-003"),
                    ),
                ),
                derived(
                    "PRD-003",
                    dependency_sources=(
                        rule_source("GEO-001"),
                    ),
                ),
            ),
        )


def test_graph_detects_cycle_across_legacy_and_typed_sources() -> None:
    with pytest.raises(
        ValueError,
        match="cyclic rule dependency detected",
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "GEO-001",
                    source_rule_ids=(
                        "PRD-003",
                    ),
                ),
                derived(
                    "PRD-003",
                    dependency_sources=(
                        rule_source("GEO-001"),
                    ),
                ),
            ),
        )


def test_graph_accepts_declared_context_policy_source() -> None:
    graph = build_rule_provenance_graph(
        records=(
            derived(
                "GEO-005",
                dependency_sources=(
                    policy_source(
                        "CP01-CONTEXTUAL-ADAPTATION"
                    ),
                ),
            ),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert graph.total_rules == 1
    assert graph.directly_observed_count == 0
    assert graph.derived_count == 1
    assert graph.context_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
    )


def test_graph_rejects_undeclared_context_policy_source() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "missing context policy source_id: "
            "CP01-CONTEXTUAL-ADAPTATION"
        ),
    ):
        build_rule_provenance_graph(
            records=(
                derived(
                    "GEO-005",
                    dependency_sources=(
                        policy_source(
                            "CP01-CONTEXTUAL-ADAPTATION"
                        ),
                    ),
                ),
            ),
        )


def test_context_policy_is_not_counted_as_rule() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            derived(
                "GEO-005",
                dependency_sources=(
                    policy_source(
                        "CP01-CONTEXTUAL-ADAPTATION"
                    ),
                ),
            ),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert graph.total_rules == 2
    assert graph.directly_observed_count == 1
    assert graph.derived_count == 1


def test_graph_accepts_mixed_rule_and_context_policy_sources() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            derived(
                "GEO-005",
                dependency_sources=(
                    rule_source("CLR-001"),
                    policy_source(
                        "CP01-CONTEXTUAL-ADAPTATION"
                    ),
                ),
            ),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert graph.total_rules == 2
    assert graph.derived_count == 1


def test_graph_accepts_shared_declared_context_policy() -> None:
    graph = build_rule_provenance_graph(
        records=(
            derived(
                "GEO-005",
                dependency_sources=(
                    policy_source(
                        "CP01-CONTEXTUAL-ADAPTATION"
                    ),
                ),
            ),
            derived(
                "CAP-004",
                dependency_sources=(
                    policy_source(
                        "CP01-CONTEXTUAL-ADAPTATION"
                    ),
                ),
            ),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    assert graph.total_rules == 2
    assert graph.derived_count == 2
    assert len(graph.context_policy_ids) == 1


def test_graph_rejects_mutable_context_policy_collection() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "context_policy_ids must be "
            "an immutable tuple"
        ),
    ):
        build_rule_provenance_graph(
            records=(
                direct("CLR-001"),
            ),
            context_policy_ids=[
                "CP01-CONTEXTUAL-ADAPTATION",
            ],
        )


@pytest.mark.parametrize(
    "invalid_policy_id",
    (
        "",
        "   ",
        None,
    ),
)
def test_graph_rejects_invalid_context_policy_identity(
    invalid_policy_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="context policy source_id must not be empty",
    ):
        build_rule_provenance_graph(
            records=(
                direct("CLR-001"),
            ),
            context_policy_ids=(
                invalid_policy_id,
            ),
        )


def test_graph_rejects_duplicate_context_policy_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate context policy source_id: "
            "CP01-CONTEXTUAL-ADAPTATION"
        ),
    ):
        build_rule_provenance_graph(
            records=(
                direct("CLR-001"),
            ),
            context_policy_ids=(
                "CP01-CONTEXTUAL-ADAPTATION",
                "CP01-CONTEXTUAL-ADAPTATION",
            ),
        )


def test_graph_preserves_declared_context_policy_order() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
            "CP02-CHANNEL-PRESENTATION",
        ),
    )

    assert graph.context_policy_ids == (
        "CP01-CONTEXTUAL-ADAPTATION",
        "CP02-CHANNEL-PRESENTATION",
    )


def test_graph_preserves_legacy_and_typed_rule_dependencies() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
            direct("LYR-001"),
            derived(
                "GEO-001",
                source_rule_ids=(
                    "CLR-001",
                ),
                dependency_sources=(
                    rule_source("LYR-001"),
                ),
            ),
        ),
    )

    assert graph.total_rules == 3
    assert graph.directly_observed_count == 2
    assert graph.derived_count == 1


def test_context_policy_registry_is_immutable() -> None:
    graph = build_rule_provenance_graph(
        records=(
            direct("CLR-001"),
        ),
        context_policy_ids=(
            "CP01-CONTEXTUAL-ADAPTATION",
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        graph.context_policy_ids = ()
