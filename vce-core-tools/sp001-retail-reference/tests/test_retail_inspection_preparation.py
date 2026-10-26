from dataclasses import FrozenInstanceError, replace
from decimal import Decimal

import pytest

from sp001.contracts.retail_inspection_preparation import (
    RetailInspectionCapacityLimitProposal as Capacity,
    RetailInspectionPreparation as Preparation,
    RetailInspectionRulePreparation as Rule,
    RetailInspectionSamplePlan as Sample,
)


def preparation():
    return Preparation(
        preparation_id="PREPARATION-TEST", revision=1,
        case_id="VM-THL-RACK-PILOT-001",
        declared_store="Suburbia Tláhuac",
        declared_operator="Aelvira",
        proposed_protocol_id="VM-RACK-THL-001",
        proposed_protocol_version=None,
        proposed_fixture_id=None,
        sample_plan=Sample(None, None, None, None, None, None),
        rules=tuple(
            Rule(f"RACK-{i:02}", f"Proposed requirement {i}", None, None, None, None)
            for i in range(1, 8)
        ),
        aggregation_proposal=(
            "One result per rule; preserve independent deviations, "
            "contradictions and incomplete evidence."
        ),
        dispute_resolver_reference=None,
        capacity_limits=(),
        closure_authority_reference=None,
        closure_blockers=("PROTOCOL_APPROVAL_PENDING",),
        candidate_evidence_ids=("IMAGE-CANDIDATE-TEST",),
    )


def test_pending_preparation_has_no_evaluations_or_approval():
    value = preparation()
    assert len(value.rules) == 7
    assert all(rule.proposed_applicability is None for rule in value.rules)
    assert all(rule.proposed_criticality is None for rule in value.rules)
    assert value.sample_plan.universe_garments is None
    assert value.sample_plan.planned_positions is None
    assert value.capacity_limits == ()
    assert value.closure_authority_reference is None
    assert not hasattr(value, "evaluations")
    assert not hasattr(value, "coverage")
    assert not hasattr(value, "approved")
    with pytest.raises(FrozenInstanceError):
        value.revision = 2


def test_plan_and_capacity_are_explicit_declarations():
    value = preparation()
    planned = replace(
        value,
        revision=2,
        sample_plan=Sample(10, 20, ("P1", "P2"), 3, "Declared method", None),
        capacity_limits=(
            Capacity(Decimal("12.5"), "kg", "SPEC-1", "Weigh", "SCALE-1"),
            Capacity(Decimal("20"), "garments", "SPEC-1", "Count", None),
        ),
    )
    assert value.sample_plan.universe_positions is None
    assert planned.capacity_limits[0].unit == "kg"
    assert planned.capacity_limits[1].unit == "garments"
    assert not hasattr(planned.capacity_limits[0], "measured_value")


@pytest.mark.parametrize("change", [
    {"universe_positions": -1},
    {"universe_garments": True},
    {"planned_positions": ("P1", "P1")},
    {"planned_garments": -1},
])
def test_rejects_invalid_sample(change):
    with pytest.raises((TypeError, ValueError)):
        replace(preparation().sample_plan, **change)


def test_rejects_sample_larger_than_declared_universe():
    with pytest.raises(ValueError):
        Sample(1, 1, ("P1", "P2"), 1, None, None)
    with pytest.raises(ValueError):
        Sample(1, 1, ("P1",), 2, None, None)


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("-1"), Decimal("NaN")])
def test_rejects_invalid_capacity(value):
    with pytest.raises(ValueError):
        Capacity(value, "kg", None, None, None)


def test_rejects_float_capacity_without_implicit_rounding():
    with pytest.raises(TypeError):
        Capacity(1.5, "kg", None, None, None)


def test_rejects_duplicate_rules():
    value = preparation()
    with pytest.raises(ValueError, match="unique"):
        replace(value, rules=(value.rules[0], value.rules[0]))


def test_rejects_duplicate_evidence_and_invalid_revision():
    value = preparation()
    with pytest.raises(ValueError):
        replace(value, candidate_evidence_ids=("E1", "E1"))
    with pytest.raises(TypeError):
        replace(value, revision=True)
