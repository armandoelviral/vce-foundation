from dataclasses import FrozenInstanceError, fields, replace

import pytest

from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_resource_link import CaseResourceLink
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)


A = CaseResourceLink("context", "retail", "CONTEXT-102")
B = CaseResourceLink("evidence", "receipt", "RECEIPT-1")


def opening():
    return CaseOpeningRequest("T-1", "CASE-1", "OBJ-1", "STORE-1", (A,))


def transition():
    return CaseTransitionRequest(
        "T-2", "CASE-1", 1, Phase.RECOMMENDATION_AVAILABLE, (B,),
    )


@pytest.mark.parametrize("factory", [opening, transition])
def test_exact_repetition_preserves_value_and_is_immutable(factory):
    value = factory()
    assert value == factory()
    assert not hasattr(value, "__dict__")
    with pytest.raises(FrozenInstanceError):
        value.case_id = "OTHER"


@pytest.mark.parametrize("field,value", [
    ("transition_id", "OTHER-T"),
    ("case_id", "OTHER-CASE"),
    ("objective_id", "OTHER-OBJECTIVE"),
    ("scope", "OTHER-STORE"),
    ("resource_links", (A, B)),
])
def test_opening_comparison_includes_every_request_field(field, value):
    original = opening()
    assert replace(original, **{field: value}) != original


@pytest.mark.parametrize("field,value", [
    ("transition_id", "OTHER-T"),
    ("case_id", "OTHER-CASE"),
    ("expected_revision", 2),
    ("to_phase", Phase.AWAITING_EXPERT_DECISION),
    ("resource_links", (A, B)),
])
def test_transition_comparison_includes_every_request_field(field, value):
    original = transition()
    assert replace(original, **{field: value}) != original


def test_same_identity_and_context_do_not_hide_changed_opening_intent():
    original = opening()
    changed = replace(original, objective_id="WITHDRAW-LOT")
    assert changed.transition_id == original.transition_id
    assert changed.resource_links == original.resource_links
    assert changed != original


def test_transition_retains_requested_additions_only():
    value = transition()
    assert value.resource_links == (B,)
    assert A not in value.resource_links


@pytest.mark.parametrize("factory", [opening, transition])
@pytest.mark.parametrize("links,error", [
    ([], TypeError),
    (("invalid",), TypeError),
    ((A, A), ValueError),
    ((B, A), ValueError),
])
def test_invalid_links_are_rejected(factory, links, error):
    with pytest.raises(error):
        replace(factory(), resource_links=links)


@pytest.mark.parametrize("value,error", [
    (True, TypeError),
    ("1", TypeError),
    (0, ValueError),
    ((1 << 64) - 1, ValueError),
])
def test_transition_requires_revision_with_successor(value, error):
    with pytest.raises(error):
        replace(transition(), expected_revision=value)


@pytest.mark.parametrize("factory", [opening, transition])
@pytest.mark.parametrize("field,value,error", [
    ("transition_id", "", ValueError),
    ("case_id", " ", ValueError),
    ("case_id", 1, TypeError),
])
def test_request_identity_validation(factory, field, value, error):
    with pytest.raises(error):
        replace(factory(), **{field: value})


def test_operation_profiles_are_explicit_and_versioned():
    assert opening().operation == "OPEN_CASE"
    assert transition().operation == "APPLY_CASE_TRANSITION"
    assert opening().schema_version == transition().schema_version == 1
    assert "schema_version" not in {field.name for field in fields(opening())}
    # A serializer must explicitly include the profile and schema version.


def test_scope_preserves_existing_contract_without_silent_normalization():
    value = replace(opening(), scope="")
    assert value.scope == ""
    assert replace(opening(), scope=" STORE-1 ") != opening()


def test_invalid_phase_is_rejected():
    with pytest.raises(TypeError):
        replace(transition(), to_phase="RECOMMENDATION_AVAILABLE")
