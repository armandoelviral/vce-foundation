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


def evidence_assessed(
    rule_id: str,
) -> RetailContextRuleProvenance:
    return RetailContextRuleProvenance(
        rule_id=rule_id,
        provenance_type=(
            RuleProvenanceType.EVIDENCE_ASSESSED
        ),
    )


def test_evidence_assessed_provenance_type_is_explicit() -> None:
    assert (
        RuleProvenanceType.EVIDENCE_ASSESSED.value
        == "EVIDENCE_ASSESSED"
    )


def test_evidence_assessed_rule_requires_no_source_rules() -> None:
    provenance = evidence_assessed(
        "GEO-004",
    )

    assert provenance.rule_id == "GEO-004"

    assert (
        provenance.provenance_type
        is RuleProvenanceType.EVIDENCE_ASSESSED
    )

    assert provenance.source_rule_ids == ()
    assert provenance.dependency_sources == ()


@pytest.mark.parametrize(
    "rule_id",
    (
        "GEO-004",
        "PHO-002",
        "CAP-001",
        "CAP-003",
        "CAP-004",
    ),
)
def test_canonical_evidence_limited_rules_are_representable(
    rule_id: str,
) -> None:
    provenance = evidence_assessed(
        rule_id,
    )

    assert provenance.rule_id == rule_id

    assert (
        provenance.provenance_type
        is RuleProvenanceType.EVIDENCE_ASSESSED
    )


def test_evidence_assessed_is_not_directly_observed() -> None:
    provenance = evidence_assessed(
        "PHO-002",
    )

    assert (
        provenance.provenance_type
        is not RuleProvenanceType.DIRECTLY_OBSERVED
    )


def test_evidence_assessed_is_not_derived() -> None:
    provenance = evidence_assessed(
        "CAP-001",
    )

    assert (
        provenance.provenance_type
        is not RuleProvenanceType.DERIVED
    )


def test_evidence_assessed_rejects_legacy_source_rules() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "evidence-assessed provenance "
            "cannot declare dependency sources"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-004",
            provenance_type=(
                RuleProvenanceType.EVIDENCE_ASSESSED
            ),
            source_rule_ids=(
                "CLR-001",
            ),
        )


def test_evidence_assessed_rejects_typed_rule_dependencies() -> None:
    source = RetailContextDependencySource(
        source_id="CLR-001",
        source_type=DependencySourceType.RULE,
    )

    with pytest.raises(
        ValueError,
        match=(
            "evidence-assessed provenance "
            "cannot declare dependency sources"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="GEO-004",
            provenance_type=(
                RuleProvenanceType.EVIDENCE_ASSESSED
            ),
            dependency_sources=(
                source,
            ),
        )


def test_evidence_assessed_rejects_context_policy_dependencies() -> None:
    source = RetailContextDependencySource(
        source_id="CP01-CONTEXTUAL-ADAPTATION",
        source_type=(
            DependencySourceType.CONTEXT_POLICY
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "evidence-assessed provenance "
            "cannot declare dependency sources"
        ),
    ):
        RetailContextRuleProvenance(
            rule_id="CAP-004",
            provenance_type=(
                RuleProvenanceType.EVIDENCE_ASSESSED
            ),
            dependency_sources=(
                source,
            ),
        )


def test_existing_directly_observed_provenance_remains_valid() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="CLR-001",
        provenance_type=(
            RuleProvenanceType.DIRECTLY_OBSERVED
        ),
    )

    assert (
        provenance.provenance_type
        is RuleProvenanceType.DIRECTLY_OBSERVED
    )


def test_existing_derived_provenance_remains_valid() -> None:
    provenance = RetailContextRuleProvenance(
        rule_id="GEO-001",
        provenance_type=(
            RuleProvenanceType.DERIVED
        ),
        source_rule_ids=(
            "CLR-001",
        ),
    )

    assert (
        provenance.provenance_type
        is RuleProvenanceType.DERIVED
    )

    assert provenance.source_rule_ids == (
        "CLR-001",
    )


def test_evidence_assessed_provenance_remains_immutable() -> None:
    provenance = evidence_assessed(
        "CAP-003",
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        provenance.rule_id = "CAP-004"


def test_provenance_vocabulary_distinguishes_three_evidence_origins() -> None:
    assert {
        provenance_type.value
        for provenance_type in RuleProvenanceType
    } == {
        "DIRECTLY_OBSERVED",
        "DERIVED",
        "EVIDENCE_ASSESSED",
    }
