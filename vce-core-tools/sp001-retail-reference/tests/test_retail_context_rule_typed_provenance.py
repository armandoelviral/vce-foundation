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
        source_type=DependencySourceType.CONTEXT_POLICY,
    )


def test_legacy_rule_dependencies_remain_compatible() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="OCC-002",
        provenance_type=RuleProvenanceType.DERIVED,
        source_rule_ids=(
            "LYR-001",
            "LYR-002",
            "OCC-001",
        ),
    )

    assert provenance.source_rule_ids == (
        "LYR-001",
        "LYR-002",
        "OCC-001",
    )

    assert provenance.dependency_sources == ()


def test_context_policy_can_support_derived_rule() -> None:
    adaptation = policy_source(
        "CP01-CONTEXTUAL-ADAPTATION"
    )

    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=RuleProvenanceType.DERIVED,
        dependency_sources=(
            adaptation,
        ),
    )

    assert provenance.source_rule_ids == ()

    assert provenance.dependency_sources == (
        adaptation,
    )

    assert (
        provenance.dependency_sources[0].source_type
        is DependencySourceType.CONTEXT_POLICY
    )


def test_typed_rule_source_can_support_derived_rule() -> None:
    layering = rule_source(
        "LYR-001"
    )

    provenance = RetailContextRuleProvenance(
        rule_id="OCC-002",
        provenance_type=RuleProvenanceType.DERIVED,
        dependency_sources=(
            layering,
        ),
    )

    assert provenance.dependency_sources == (
        layering,
    )


def test_rule_and_policy_dependencies_can_be_combined() -> None:
    layering = rule_source(
        "LYR-001"
    )

    adaptation = policy_source(
        "CP01-CONTEXTUAL-ADAPTATION"
    )

    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=RuleProvenanceType.DERIVED,
        dependency_sources=(
            layering,
            adaptation,
        ),
    )

    assert tuple(
        source.source_type
        for source in provenance.dependency_sources
    ) == (
        DependencySourceType.RULE,
        DependencySourceType.CONTEXT_POLICY,
    )


def test_legacy_rule_and_typed_policy_can_coexist() -> None:
    adaptation = policy_source(
        "CP01-CONTEXTUAL-ADAPTATION"
    )

    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=RuleProvenanceType.DERIVED,
        source_rule_ids=(
            "LYR-001",
        ),
        dependency_sources=(
            adaptation,
        ),
    )

    assert provenance.source_rule_ids == (
        "LYR-001",
    )

    assert provenance.dependency_sources == (
        adaptation,
    )


def test_direct_observation_rejects_typed_dependencies() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "directly observed provenance "
            "cannot declare source rules"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="CLR-001",
            provenance_type=(
                RuleProvenanceType.DIRECTLY_OBSERVED
            ),
            dependency_sources=(
                policy_source(
                    "CP01-CONTEXTUAL-ADAPTATION"
                ),
            ),
        )


def test_derived_rule_without_any_source_remains_invalid() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "derived provenance requires source rules"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-005",
            provenance_type=RuleProvenanceType.DERIVED,
        )


def test_provenance_rejects_mutable_typed_source_collection() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "dependency_sources must be an immutable tuple"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-005",
            provenance_type=RuleProvenanceType.DERIVED,
            dependency_sources=[
                policy_source(
                    "CP01-CONTEXTUAL-ADAPTATION"
                ),
            ],
        )


def test_provenance_rejects_invalid_typed_source_element() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "every dependency source must be a "
            "RetailContextDependencySource"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-005",
            provenance_type=RuleProvenanceType.DERIVED,
            dependency_sources=(
                "CP01-CONTEXTUAL-ADAPTATION",
            ),
        )


def test_provenance_rejects_duplicate_typed_sources() -> None:
    adaptation = policy_source(
        "CP01-CONTEXTUAL-ADAPTATION"
    )

    with pytest.raises(
        ValueError,
        match=(
            "duplicate dependency source: "
            "CONTEXT_POLICY:CP01-CONTEXTUAL-ADAPTATION"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-005",
            provenance_type=RuleProvenanceType.DERIVED,
            dependency_sources=(
                adaptation,
                adaptation,
            ),
        )


def test_provenance_rejects_duplicate_rule_across_representations() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate source rule_id: "
            "LYR-001"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="OCC-002",
            provenance_type=RuleProvenanceType.DERIVED,
            source_rule_ids=(
                "LYR-001",
            ),
            dependency_sources=(
                rule_source(
                    "LYR-001"
                ),
            ),
        )


def test_provenance_rejects_typed_rule_self_reference() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "derived rule cannot depend on itself: "
            "GEO-005"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-005",
            provenance_type=RuleProvenanceType.DERIVED,
            dependency_sources=(
                rule_source(
                    "GEO-005"
                ),
            ),
        )


def test_typed_dependency_collection_remains_immutable() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="GEO-005",
        provenance_type=RuleProvenanceType.DERIVED,
        dependency_sources=(
            policy_source(
                "CP01-CONTEXTUAL-ADAPTATION"
            ),
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        provenance.dependency_sources = ()
