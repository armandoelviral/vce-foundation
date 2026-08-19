from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_dependency_source import (
    DependencySourceType,
    RetailContextDependencySource,
)


def test_rule_source_preserves_identity_and_type() -> None:
    source = RetailContextDependencySource(
        source_id="LYR-001",
        source_type=DependencySourceType.RULE,
    )

    assert source.source_id == "LYR-001"

    assert (
        source.source_type
        is DependencySourceType.RULE
    )


def test_context_policy_source_preserves_identity_and_type() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=DependencySourceType.CONTEXT_POLICY,
    )

    assert (
        source.source_id
        == "CP01-CONTEXTUAL-ADAPTATION"
    )

    assert (
        source.source_type
        is DependencySourceType.CONTEXT_POLICY
    )


def test_rule_and_policy_sources_with_same_identity_remain_distinct() -> None:
    rule_source = RetailContextDependencySource(
        source_id="SHARED-SOURCE-001",
        source_type=DependencySourceType.RULE,
    )

    policy_source = RetailContextDependencySource(
        source_id="SHARED-SOURCE-001",
        source_type=DependencySourceType.CONTEXT_POLICY,
    )

    assert rule_source != policy_source


@pytest.mark.parametrize(
    "invalid_identity",
    ("", "   ", 123),
)
def test_source_rejects_invalid_identity(
    invalid_identity: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="source_id must not be empty",
    ):
        RetailContextDependencySource(
            source_id=invalid_identity,
            source_type=DependencySourceType.RULE,
        )


def test_source_rejects_untyped_source_classification() -> None:
    with pytest.raises(
        TypeError,
        match="source_type must be a DependencySourceType",
    ):
        RetailContextDependencySource(
            source_id="LYR-001",
            source_type="RULE",
        )


def test_source_is_immutable() -> None:
    source = RetailContextDependencySource(
        source_id="LYR-001",
        source_type=DependencySourceType.RULE,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        source.source_id = "LYR-002"


def test_source_vocabulary_is_exact() -> None:
    assert {
        source_type.value
        for source_type in DependencySourceType
    } == {
        "RULE",
        "CONTEXT_POLICY",
    }


def test_context_policy_is_not_treated_as_rule() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=DependencySourceType.CONTEXT_POLICY,
    )

    assert (
        source.source_type
        is not DependencySourceType.RULE
    )


def test_source_does_not_claim_policy_authority() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=DependencySourceType.CONTEXT_POLICY,
    )

    assert not hasattr(
        source,
        "authority_granted",
    )

    assert not hasattr(
        source,
        "customer_accepted",
    )

    assert not hasattr(
        source,
        "commercial_revenue",
    )


def test_source_identity_preserves_declared_customer_label() -> None:
    source = RetailContextDependencySource(
        source_id="CUSTOMER-CONTEXT-POLICY-007",
        source_type=DependencySourceType.CONTEXT_POLICY,
    )

    assert (
        source.source_id
        == "CUSTOMER-CONTEXT-POLICY-007"
    )
