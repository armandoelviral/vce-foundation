import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservationMethod as Method,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
    deserialize_retail_inspection_observation as deserialize,
)


def dump(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    )


def test_roundtrip_preserves_full_content_and_canonical_document():
    original = observation(
        description="Texto literal: á, ñ\nSegunda línea.",
        limitations=("Sin medición.", "Zona oculta."),
        evidence_ids=("PHOTO-2", "PHOTO-1"),
    )
    document = serialize(original)
    recovered = deserialize(document)
    assert recovered == original
    assert recovered is not original
    assert serialize(recovered) == document
    assert recovered.declared_observer == original.declared_observer
    assert recovered.limitations == original.limitations
    assert recovered.evidence_ids == ("PHOTO-2", "PHOTO-1")


def test_direct_inspection_preserves_empty_collections():
    original = observation(
        method=Method.DIRECT_INSPECTION, evidence_ids=(), limitations=(),
    )
    assert deserialize(serialize(original)) == original


@pytest.mark.parametrize("fold", [0, 1])
def test_preserves_named_zone_and_ambiguous_time(fold):
    instant = datetime(
        2025, 11, 2, 1, 30,
        tzinfo=ZoneInfo("America/New_York"), fold=fold,
    )
    original = observation(observed_at=instant, recorded_at=instant)
    recovered = deserialize(serialize(original))
    for name in ("observed_at", "recorded_at"):
        value = getattr(recovered, name)
        assert value.tzinfo.key == "America/New_York"
        assert value.fold == fold
        assert value.isoformat() == instant.isoformat()


def test_preserves_fixed_offset():
    instant = datetime(
        2026, 1, 1, 12,
        tzinfo=timezone(timedelta(hours=-6)),
    )
    original = observation(observed_at=instant, recorded_at=instant)
    recovered = deserialize(serialize(original))
    assert recovered.observed_at.isoformat() == instant.isoformat()


@pytest.mark.parametrize("version", [2, True, "1", None])
def test_rejects_unsupported_schema(version):
    data = json.loads(serialize(observation()))
    data["schema_version"] = version
    with pytest.raises(ValueError):
        deserialize(dump(data))


def test_rejects_duplicate_keys():
    document = serialize(observation()).replace(
        '"schema_version":1',
        '"schema_version":1,"schema_version":1',
    )
    with pytest.raises(ValueError, match="duplicate"):
        deserialize(document)


@pytest.mark.parametrize("location", ["envelope", "observation"])
def test_rejects_unknown_fields(location):
    data = json.loads(serialize(observation()))
    target = data if location == "envelope" else data["observation"]
    target["approved"] = "yes"
    with pytest.raises(ValueError):
        deserialize(dump(data))


def test_rejects_missing_field():
    data = json.loads(serialize(observation()))
    del data["observation"]["scope"]
    with pytest.raises(ValueError):
        deserialize(dump(data))


@pytest.mark.parametrize("name,value,error", [
    ("description", "", ValueError),
    ("observation_version", True, ValueError),
    ("method", "UNKNOWN", ValueError),
    ("method", 1, ValueError),
    ("declared_observer", "ACTOR", TypeError),
    ("evidence_ids", {"type": "tuple", "items": []}, ValueError),
    ("evidence_ids", {"type": "tuple", "items": ["E", "E"]}, ValueError),
])
def test_recovery_reapplies_validation(name, value, error):
    data = json.loads(serialize(observation()))
    data["observation"][name] = value
    with pytest.raises(error):
        deserialize(dump(data))


def test_rejects_naive_datetime():
    data = json.loads(serialize(observation()))
    data["observation"]["observed_at"]["iso"] = "2026-01-01T12:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        deserialize(dump(data))


def test_rejects_recording_before_observation():
    data = json.loads(serialize(observation()))
    data["observation"]["recorded_at"]["iso"] = "2025-01-01T12:00:00+00:00"
    with pytest.raises(ValueError, match="must not precede"):
        deserialize(dump(data))


@pytest.mark.parametrize("document", [
    "[]", "null", "{}",
    '{"schema_version":NaN,"observation":null}',
    '{"schema_version":1.0,"observation":null}',
])
def test_rejects_invalid_documents(document):
    with pytest.raises(ValueError):
        deserialize(document)


def test_rejects_noncanonical_whitespace():
    with pytest.raises(ValueError, match="canonical"):
        deserialize(serialize(observation()) + "\n")


def test_requires_nominal_input_and_string_document():
    with pytest.raises(TypeError):
        serialize({})
    with pytest.raises(TypeError):
        deserialize(b"{}")


def test_changed_description_is_content_not_cryptographic_tampering_detection():
    original = observation()
    changed = replace(original, description="Another declared observation.")
    assert serialize(original) != serialize(changed)
    assert deserialize(serialize(changed)) == changed
