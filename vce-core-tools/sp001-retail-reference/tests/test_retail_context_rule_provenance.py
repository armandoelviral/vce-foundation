from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.retail_context_rule_provenance import (
    RetailContextRuleProvenance,
    RuleProvenanceType,
)


def test_direct_observation_preserves_rule_identity() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="RULE-CLR-001",
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )

    assert provenance.rule_id == "RULE-CLR-001"

    assert (
        provenance.provenance_type
        is RuleProvenanceType.DIRECTLY_OBSERVED
    )

    assert provenance.source_rule_ids == ()


def test_derived_rule_preserves_explicit_source_rules() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="RULE-PRD-003",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=(
            "RULE-CLR-001",
            "RULE-PRD-001",
        ),
    )

    assert provenance.rule_id == "RULE-PRD-003"

    assert (
        provenance.provenance_type
        is RuleProvenanceType.DERIVED
    )

    assert provenance.source_rule_ids == (
        "RULE-CLR-001",
        "RULE-PRD-001",
    )


def test_derived_rule_requires_source_identity() -> None:
    with pytest.raises(
        ValueError,
        match="derived provenance requires source rules",
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-PRD-003",
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
        )


def test_direct_rule_rejects_derived_source_identities() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "directly observed provenance "
            "cannot declare source rules"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-CLR-001",
            provenance_type=(
                RuleProvenanceType.DIRECTLY_OBSERVED
            ),
            source_rule_ids=(
                "RULE-CLR-002",
            ),
        )


def test_provenance_rejects_duplicate_source_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate source rule_id: "
            "RULE-CLR-001"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-PRD-003",
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            source_rule_ids=(
                "RULE-CLR-001",
                "RULE-CLR-001",
            ),
        )


def test_provenance_rejects_direct_self_reference() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "derived rule cannot depend on itself: "
            "RULE-PRD-003"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-PRD-003",
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            source_rule_ids=(
                "RULE-PRD-003",
            ),
        )


def test_provenance_rejects_mutable_source_collection() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "source_rule_ids must be an immutable tuple"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-PRD-003",
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            source_rule_ids=[
                "RULE-CLR-001",
            ],
        )


@pytest.mark.parametrize(
    "invalid_source",
    ("", "   ", 123),
)
def test_provenance_rejects_invalid_source_identity(
    invalid_source: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="source rule_id must not be empty",
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-PRD-003",
            provenance_type=(
                RuleProvenanceType.DERIVED
            ),
            source_rule_ids=(
                invalid_source,
            ),
        )


@pytest.mark.parametrize(
    "invalid_identity",
    ("", "   "),
)
def test_provenance_rejects_invalid_rule_identity(
    invalid_identity: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="rule_id must not be empty",
    ):
        RetailContextRuleProvenance(
            rule_id=invalid_identity,
            provenance_type=(
                RuleProvenanceType.DIRECTLY_OBSERVED
            ),
        )


def test_provenance_rejects_untyped_classification() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "provenance_type must be a RuleProvenanceType"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="RULE-CLR-001",
            provenance_type="DIRECTLY_OBSERVED",
        )


def test_provenance_preserves_declared_source_order() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="RULE-PRD-003",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=(
            "RULE-LYR-002",
            "RULE-CLR-001",
            "RULE-PRD-001",
        ),
    )

    assert provenance.source_rule_ids == (
        "RULE-LYR-002",
        "RULE-CLR-001",
        "RULE-PRD-001",
    )


def test_provenance_is_immutable() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="RULE-CLR-001",
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        provenance.rule_id = "RULE-CLR-002"


def test_provenance_vocabulary_is_exact() -> None:
    assert {
        classification.value
        for classification in RuleProvenanceType
    } == {
        "DIRECTLY_OBSERVED",
        "DERIVED",
        "EVIDENCE_ASSESSED",
    }


def test_provenance_does_not_claim_operational_independence() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="RULE-PRD-003",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=(
            "RULE-CLR-001",
        ),
    )

    assert not hasattr(
        provenance,
        "independent_interventions",
    )

    assert not hasattr(
        provenance,
        "commercial_revenue",
    )

    assert not hasattr(
        provenance,
        "customer_accepted",
    )
