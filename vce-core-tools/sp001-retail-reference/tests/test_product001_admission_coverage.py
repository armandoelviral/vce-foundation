"""PRODUCT-001 additional admission boundary coverage."""

from dataclasses import replace

import pytest

from product001_admission_fixtures import make_valid_admission_case
from sp001.services.product001_planogram_admission import (
    _compose_planogram_expected_state_from_decision,
)


def admit(case):
    return _compose_planogram_expected_state_from_decision(
        expected_state_id="PRODUCT-001-COVERAGE-001",
        expected_state_version=1,
        rule=case.rule,
        snapshot=case.snapshot,
        retrieval_decision=case.decision,
        provenance_bindings=case.bindings,
        planogram_dimension_ids=case.planogram_dimension_ids,
    )


def test_included_decision_with_false_digest_is_rejected():
    case = make_valid_admission_case()
    contradictory = replace(
        case.decision,
        content_bytes_match_digest=False,
    )

    assert contradictory.content_bytes_match_digest is False

    with pytest.raises(ValueError):
        admit(replace(case, decision=contradictory))


def test_undeclared_extra_binding_is_rejected():
    from sp001.contracts.retail_context_observation_provenance_binding import (
        bind_retail_context_observation_provenance,
    )

    case = make_valid_admission_case()
    inventory = next(
        dimension
        for dimension in case.snapshot.dimensions
        if dimension.dimension_id == "DIM-INVENTORY-001"
    )

    provenance = replace(
        case.bindings[0].provenance,
        observation_id="PRODUCT-001-UNDECLARED-OBS",
        dimension_id=inventory.dimension_id,
    )

    extra = bind_retail_context_observation_provenance(
        snapshot=case.snapshot,
        provenance=provenance,
    )

    altered = replace(
        case,
        bindings=case.bindings + (extra,),
    )

    assert len(altered.bindings) == 2
    assert inventory.dimension_id not in altered.planogram_dimension_ids

    with pytest.raises(ValueError):
        admit(altered)


def test_empty_planogram_dimension_selection_is_rejected():
    case = replace(
        make_valid_admission_case(),
        planogram_dimension_ids=(),
    )

    with pytest.raises(ValueError, match="(?i)dimension"):
        admit(case)
