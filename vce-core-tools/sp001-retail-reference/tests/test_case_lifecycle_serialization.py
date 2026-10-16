import json
from dataclasses import replace

import pytest

from test_case_lifecycle_completion import opening, completion
from sp001.infrastructure.case_lifecycle_serialization import (
    serialize_case_lifecycle as dump,
    deserialize_case_lifecycle as load,
)


@pytest.mark.parametrize("value", [
    opening().request, completion().request, opening(), completion(),
])
def test_exact_typed_round_trip(value):
    document = dump(value)
    recovered = load(document)
    assert type(recovered) is type(value)
    assert recovered == value
    assert dump(recovered) == document


def test_unicode_and_delimiters_are_preserved_without_normalization():
    value = replace(
        opening().request,
        objective_id="OBJ:á|中",
        scope=" tienda|a:b ",
    )
    assert load(dump(value)) == value
    assert dump(value).isascii()


def test_all_request_fields_affect_serialization():
    value = opening().request
    for field, changed in (
        ("transition_id", "OTHER-T"),
        ("case_id", "OTHER-C"),
        ("objective_id", "OTHER-O"),
        ("scope", "OTHER-S"),
        ("resource_links", ()),
    ):
        assert dump(replace(value, **{field: changed})) != dump(value)


def test_nested_previous_state_and_exact_additions_survive():
    value = load(dump(completion()))
    assert value.previous_state == completion().previous_state
    assert value.request.resource_links == completion().request.resource_links
    assert value.state.resource_links == completion().state.resource_links


@pytest.mark.parametrize("mutation", ["unknown", "missing", "schema", "type"])
def test_unexpected_structure_is_rejected(mutation):
    raw = json.loads(dump(opening().request))
    if mutation == "unknown":
        raw["value"]["fields"]["price"] = "14.50"
    elif mutation == "missing":
        del raw["value"]["fields"]["scope"]
    elif mutation == "schema":
        raw["schema"] = "sp001.case-lifecycle.v2"
    else:
        raw["value"]["type"] = "unknown"
    with pytest.raises(ValueError):
        load(json.dumps(raw, sort_keys=True, separators=(",", ":")).encode())


def test_duplicate_nested_keys_are_rejected():
    document = dump(opening().request)
    document = document.replace(
        b'"scope":"STORE-1"',
        b'"scope":"STORE-1","scope":"OTHER"',
    )
    with pytest.raises(ValueError, match="duplicate"):
        load(document)


def test_noncanonical_whitespace_is_rejected():
    with pytest.raises(ValueError, match="canonical"):
        load(dump(opening()) + b"\n")


@pytest.mark.parametrize("replacement", [b"true", b"1.0", b"NaN"])
def test_boolean_float_and_nonfinite_revision_are_rejected(replacement):
    document = dump(completion().request)
    document = document.replace(b'"expected_revision":1', (
        b'"expected_revision":' + replacement
    ))
    with pytest.raises(ValueError):
        load(document)


def test_contradictory_nested_completion_is_rejected():
    raw = json.loads(dump(completion()))
    raw["value"]["fields"]["state"]["fields"]["scope"] = "OTHER"
    document = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
    with pytest.raises(ValueError):
        load(document)


def test_invalid_root_and_input_types_are_rejected():
    with pytest.raises(TypeError):
        dump(opening().state)
    with pytest.raises(TypeError):
        load("{}")
