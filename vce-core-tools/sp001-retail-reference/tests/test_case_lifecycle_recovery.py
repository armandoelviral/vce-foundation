from dataclasses import replace

import pytest

from test_case_lifecycle_completion import opening, completion, A, B
from sp001.contracts.case_lifecycle_execution_store import (
    CaseLifecycleExecutionStore, CaseLifecycleRequestConflict,
)
from sp001.services.case_lifecycle_recovery import (
    match_case_lifecycle_completion as match,
)


@pytest.mark.parametrize("factory", [opening, completion])
def test_exact_request_recovers_original_completion_reference(factory):
    original = factory()
    assert match(
        request=replace(original.request), completion=original,
    ) is original


@pytest.mark.parametrize("field,value", [
    ("objective_id", "OTHER-OBJECTIVE"),
    ("scope", "OTHER-STORE"),
    ("case_id", "OTHER-CASE"),
    ("resource_links", (A, B)),
])
def test_same_opening_identity_with_changed_content_is_conflict(field, value):
    original = opening()
    changed = replace(original.request, **{field: value})
    with pytest.raises(CaseLifecycleRequestConflict):
        match(request=changed, completion=original)


@pytest.mark.parametrize("field,value", [
    ("expected_revision", 2),
    ("resource_links", ()),
    ("case_id", "OTHER-CASE"),
])
def test_same_transition_identity_with_changed_content_is_conflict(field, value):
    original = completion()
    with pytest.raises(CaseLifecycleRequestConflict):
        match(
            request=replace(original.request, **{field: value}),
            completion=original,
        )


def test_different_operation_with_same_identity_is_conflict():
    original = opening()
    changed = replace(
        completion().request,
        transition_id=original.request.transition_id,
    )
    with pytest.raises(CaseLifecycleRequestConflict):
        match(request=changed, completion=original)


def test_absence_is_returned_without_constructing_a_result():
    assert match(request=opening().request, completion=None) is None


def test_wrong_record_identity_is_invalid_retrieval_not_content_conflict():
    original = opening()
    with pytest.raises(ValueError, match="different transition identity"):
        match(
            request=replace(original.request, transition_id="OTHER-T"),
            completion=original,
        )


@pytest.mark.parametrize("candidate,result", [
    (object(), None),
    (opening().request, object()),
])
def test_invalid_nominal_values_are_rejected(candidate, result):
    with pytest.raises(TypeError):
        match(request=candidate, completion=result)


def test_original_result_does_not_depend_on_a_later_current_snapshot():
    original = completion()
    later_snapshot = replace(original.state, revision=3)
    recovered = match(request=original.request, completion=original)
    assert recovered.state.revision == 2
    assert later_snapshot.revision == 3
    assert recovered is original


def test_objects_without_execution_and_recovery_do_not_satisfy_port():
    assert not isinstance(object(), CaseLifecycleExecutionStore)
