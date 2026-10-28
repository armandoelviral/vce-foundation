import json
from dataclasses import fields

from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
    RetailInspectionObservationMethod,
)
from sp001.infrastructure.retail_rule_evaluation_serialization import (
    _decode,
    _encode,
    _exact_keys,
    _invalid_number,
    _unique_object,
)


def serialize_retail_inspection_observation(
    observation: RetailInspectionObservation,
) -> str:
    """Encode declared content; performs no authentication or persistence."""
    if type(observation) is not RetailInspectionObservation:
        raise TypeError("observation must be a RetailInspectionObservation")

    encoded = {
        field.name: _encode(getattr(observation, field.name))
        for field in fields(observation)
        if field.name != "method"
    }
    encoded["method"] = observation.method.value
    return json.dumps(
        {"schema_version": 1, "observation": encoded},
        sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def deserialize_retail_inspection_observation(
    document: str,
) -> RetailInspectionObservation:
    """Recover canonical content and reapply constructor validation."""
    if type(document) is not str:
        raise TypeError("document must be a string")

    envelope = json.loads(
        document,
        object_pairs_hook=_unique_object,
        parse_float=_invalid_number,
        parse_constant=_invalid_number,
    )
    if type(envelope) is not dict:
        raise ValueError("envelope must be an object")
    _exact_keys(envelope, {"schema_version", "observation"})
    if (
        type(envelope["schema_version"]) is not int
        or envelope["schema_version"] != 1
    ):
        raise ValueError("unsupported schema version")

    raw = envelope["observation"]
    if type(raw) is not dict:
        raise ValueError("observation must be an object")
    _exact_keys(raw, {
        field.name for field in fields(RetailInspectionObservation)
    })
    if type(raw["method"]) is not str:
        raise ValueError("method must be a string")

    values = {
        name: _decode(value)
        for name, value in raw.items()
        if name != "method"
    }
    values["method"] = RetailInspectionObservationMethod(raw["method"])
    observation = RetailInspectionObservation(**values)

    if serialize_retail_inspection_observation(observation) != document:
        raise ValueError("document must use canonical format")
    return observation
