from dataclasses import replace
from decimal import Decimal

import pytest

import test_retail_inspection_preparation as setup

from sp001.contracts.retail_inspection_preparation import (
    RetailInspectionCapacityLimitProposal as Capacity,
    RetailInspectionSamplePlan as Sample,
)


def test_reference_to_authority_does_not_grant_approval():
    value = setup.preparation()
    proposal = replace(
        value,
        dispute_resolver_reference="DECLARED-RESOLVER",
        closure_authority_reference="DECLARED-AUTHORITY",
    )
    assert proposal.closure_authority_reference == "DECLARED-AUTHORITY"
    assert not hasattr(proposal, "approved")
    assert not hasattr(proposal, "authorize_closure")
    assert not hasattr(proposal, "closed")


def test_partial_sample_plan_does_not_fabricate_execution():
    value = setup.preparation()
    proposal = replace(
        value,
        sample_plan=Sample(
            universe_positions=10, universe_garments=20,
            planned_positions=("P1", "P2"), planned_garments=3,
            selection_method="Selection proposed for review",
            required_coverage=None,
        ),
    )
    assert proposal.sample_plan.planned_positions == ("P1", "P2")
    assert not hasattr(proposal.sample_plan, "reviewed_positions")
    assert not hasattr(proposal.sample_plan, "observed_garments")
    assert not hasattr(proposal, "coverage")


def test_combined_capacity_limits_remain_separate_without_conversion():
    value = setup.preparation()
    limits = (
        Capacity(Decimal("12.5"), "kg", "SPEC", "Weigh", "SCALE"),
        Capacity(Decimal("20"), "garments", "SPEC", "Count", None),
    )
    proposal = replace(value, capacity_limits=limits)
    assert proposal.capacity_limits == limits
    assert proposal.capacity_limits[0].unit == "kg"
    assert proposal.capacity_limits[1].unit == "garments"
    assert not hasattr(proposal.capacity_limits[0], "measured_value")


def test_rule_order_preserved_without_creating_aggregate_results():
    value = setup.preparation()
    reordered = replace(value, rules=tuple(reversed(value.rules)))
    assert tuple(rule.rule_id for rule in reordered.rules) == tuple(
        reversed(tuple(rule.rule_id for rule in value.rules))
    )
    assert not hasattr(reordered, "evaluations")
    assert not hasattr(reordered, "aggregate_result")


@pytest.mark.parametrize("universe,planned,accepted", [
    (0, 0, True), (0, 1, False),
    (5, 5, True), (5, 6, False),
    (None, 6, True),
])
def test_declared_garment_plan_cannot_exceed_known_universe(
    universe, planned, accepted,
):
    arguments = (None, universe, None, planned, None, None)
    if accepted:
        assert Sample(*arguments).planned_garments == planned
    else:
        with pytest.raises(ValueError, match="exceed"):
            Sample(*arguments)
