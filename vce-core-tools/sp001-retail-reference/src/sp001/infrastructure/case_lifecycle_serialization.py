import json
from dataclasses import fields

from sp001.contracts.case_authoritative_state import CaseAuthoritativeState
from sp001.contracts.case_lifecycle_completion import CaseLifecycleCompletion
from sp001.contracts.case_lifecycle_phase import CaseLifecyclePhase
from sp001.contracts.case_lifecycle_request import (
    CaseOpeningRequest, CaseTransitionRequest,
)
from sp001.contracts.case_lifecycle_transition_record import (
    CaseLifecycleTransitionRecord,
)
from sp001.contracts.case_resource_link import CaseResourceLink


_SCHEMA = "sp001.case-lifecycle.v1"
_TYPES = {
    "opening-request": CaseOpeningRequest,
    "transition-request": CaseTransitionRequest,
    "completion": CaseLifecycleCompletion,
    "state": CaseAuthoritativeState,
    "transition-record": CaseLifecycleTransitionRecord,
    "resource-link": CaseResourceLink,
}
_TAGS = {value: key for key, value in _TYPES.items()}
_ROOTS = (CaseOpeningRequest, CaseTransitionRequest, CaseLifecycleCompletion)


def _encode(value):
    if type(value) in _TAGS:
        return {
            "type": _TAGS[type(value)],
            "fields": {
                field.name: _encode(getattr(value, field.name))
                for field in fields(value)
            },
        }
    if type(value) is CaseLifecyclePhase:
        return {"type": "phase", "value": value.value}
    if type(value) is tuple:
        return [_encode(item) for item in value]
    if value is None or type(value) in (str, int):
        return value
    raise TypeError("unsupported lifecycle value")


def serialize_case_lifecycle(value) -> bytes:
    if type(value) not in _ROOTS:
        raise TypeError("root must be an exact lifecycle request or completion")
    return json.dumps(
        {"schema": _SCHEMA, "value": _encode(value)},
        ensure_ascii=True, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("ascii")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _invalid_number(value):
    raise ValueError("unsupported JSON number")


def _decode(value):
    if value is None or type(value) in (str, int):
        return value
    if type(value) is list:
        return tuple(_decode(item) for item in value)
    if type(value) is not dict:
        raise ValueError("unsupported lifecycle document value")
    tag = value.get("type")
    if tag == "phase":
        if set(value) != {"type", "value"} or type(value["value"]) is not str:
            raise ValueError("invalid phase document")
        return CaseLifecyclePhase(value["value"])
    if type(tag) is not str or tag not in _TYPES:
        raise ValueError("unknown lifecycle type")
    cls = _TYPES[tag]
    if set(value) != {"type", "fields"} or type(value["fields"]) is not dict:
        raise ValueError("invalid typed document")
    expected = {field.name for field in fields(cls)}
    if set(value["fields"]) != expected:
        raise ValueError("unexpected lifecycle fields")
    try:
        return cls(**{
            name: _decode(item) for name, item in value["fields"].items()
        })
    except TypeError as error:
        raise ValueError("invalid lifecycle field type") from error


def deserialize_case_lifecycle(document: bytes):
    if type(document) is not bytes:
        raise TypeError("document must be bytes")
    try:
        raw = json.loads(
            document.decode("ascii"),
            object_pairs_hook=_unique_object,
            parse_float=_invalid_number,
            parse_constant=_invalid_number,
        )
        if (
            type(raw) is not dict
            or set(raw) != {"schema", "value"}
            or raw["schema"] != _SCHEMA
        ):
            raise ValueError("unsupported lifecycle schema")
        value = _decode(raw["value"])
        if type(value) not in _ROOTS:
            raise ValueError("invalid lifecycle root")
        if serialize_case_lifecycle(value) != document:
            raise ValueError("document is not canonical")
        return value
    except (UnicodeError, RecursionError) as error:
        raise ValueError("invalid lifecycle encoding") from error
