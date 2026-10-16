from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase as Phase
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink


A = CaseResourceLink("context", "retail", "CONTEXT-102")
B = CaseResourceLink("evidence", "receipt", "RECEIPT-1")


def opening():
    request = CaseOpeningRequest("T-1", "CASE-1", "OBJ-1", "STORE-1", (A,))
    state = CaseAuthoritativeState(
        "CASE-1", "OBJ-1", "STORE-1", Phase.CASE_OPENED, 1, (A,),
    )
    record = CaseLifecycleTransitionRecord(
        "CASE-1", "T-1", 1, None, Phase.CASE_OPENED, (A,),
    )
    return CaseLifecycleCompletion(request, state, record)


def completion():
    previous = opening().state
    request = CaseTransitionRequest(
        "T-2", "CASE-1", 1, Phase.RECOMMENDATION_AVAILABLE, (B,),
    )
    state = replace(
        previous, revision=2, phase=Phase.RECOMMENDATION_AVAILABLE,
        resource_links=(A, B),
    )
    record = CaseLifecycleTransitionRecord(
        "CASE-1", "T-2", 2, Phase.CASE_OPENED,
        Phase.RECOMMENDATION_AVAILABLE, (A, B),
    )
    return CaseLifecycleCompletion(request, state, record, previous)


@pytest.mark.parametrize("factory", [opening, completion])
def test_exact_binding_is_immutable_and_preserves_references(factory):
    value = factory()
    assert replace(value) == value
    assert replace(value).request is value.request
    assert not hasattr(value, "__dict__")
    with pytest.raises(FrozenInstanceError):
        value.state = None


@pytest.mark.parametrize("field,value", [
    ("objective_id", "OTHER-OBJECTIVE"),
    ("scope", "OTHER-STORE"),
    ("transition_id", "OTHER-TRANSITION"),
    ("case_id", "OTHER-CASE"),
])
def test_same_context_cannot_hide_changed_opening_request(field, value):
    original = opening()
    with pytest.raises(ValueError):
        replace(
            original,
            request=replace(original.request, **{field: value}),
        )


def test_transition_preserves_requested_additions_separately():
    value = completion()
    assert value.request.resource_links == (B,)
    assert value.previous_state.resource_links == (A,)
    assert value.state.resource_links == (A, B)


@pytest.mark.parametrize("field,value", [
    ("expected_revision", 2),
    ("to_phase", Phase.AWAITING_EXPERT_DECISION),
    ("resource_links", ()),
])
def test_changed_transition_request_cannot_reuse_result(field, value):
    original = completion()
    with pytest.raises(ValueError):
        replace(
            original,
            request=replace(original.request, **{field: value}),
        )


def test_missing_previous_state_is_rejected():
    with pytest.raises(ValueError):
        replace(completion(), previous_state=None)


def test_opening_cannot_claim_previous_state():
    value = opening()
    with pytest.raises(ValueError):
        replace(value, previous_state=value.state)


def test_dropped_previous_link_is_rejected_even_if_result_records_agree():
    value = completion()
    with pytest.raises(ValueError):
        replace(
            value,
            state=replace(value.state, resource_links=(B,)),
            transition=replace(value.transition, resource_links=(B,)),
        )


def test_existing_link_cannot_be_claimed_as_new():
    value = completion()
    with pytest.raises(ValueError):
        replace(
            value,
            request=replace(value.request, resource_links=(A, B)),
        )


@pytest.mark.parametrize("field", ["objective_id", "scope"])
def test_transition_cannot_silently_change_case_context(field):
    value = completion()
    with pytest.raises(ValueError):
        replace(value, state=replace(value.state, **{field: "OTHER"}))


@pytest.mark.parametrize("field", ["request", "state", "transition", "previous_state"])
def test_invalid_nominal_values_are_rejected(field):
    with pytest.raises(TypeError):
        replace(completion(), **{field: object()})
