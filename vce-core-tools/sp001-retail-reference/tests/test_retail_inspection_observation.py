from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone

import pytest

from sp001.contracts.retail_inspection_observation import (
    RetailInspectionObservation,
    RetailInspectionObservationMethod as Method,
)
from sp001.contracts.retail_process_actor import ActorType, RetailProcessActor
from sp001.contracts.retail_process_role import RetailProcessRole


def observation(**overrides):
    instant = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    values = dict(
        observation_id="OBS-1",
        observation_version=1,
        case_id="CASE-1",
        subject_reference="FIXTURE-1/ZONE-A",
        method=Method.EVIDENCE_REVIEW,
        description="A graphic is visible above the displayed products.",
        scope="Visible front of zone A in the supplied photograph.",
        limitations=("Dimensions were not measured.",),
        declared_observer=RetailProcessActor(
            "ACTOR", "CUSTOMER", ActorType.HUMAN, "ORG",
            RetailProcessRole("ROLE", "CUSTOMER", "Observer"),
        ),
        observed_at=instant,
        recorded_at=instant + timedelta(minutes=1),
        evidence_ids=("PHOTO-1",),
    )
    values.update(overrides)
    return RetailInspectionObservation(**values)


def test_preserves_description_scope_actor_and_dates_without_verdict():
    item = observation()
    assert item.description == (
        "A graphic is visible above the displayed products."
    )
    assert item.subject_reference == "FIXTURE-1/ZONE-A"
    assert item.declared_observer.actor_id == "ACTOR"
    assert item.recorded_at > item.observed_at
    assert item.evidence_ids == ("PHOTO-1",)
    names = {field.name for field in fields(item)}
    assert not names & {
        "status", "result", "criterion", "approval",
        "authenticated_principal", "effective_from", "snapshot_id",
    }


def test_preserves_literal_content_without_normalization():
    text = "  First line\nSecond line  "
    item = observation(description=text, scope=text, limitations=(text,))
    assert item.description == text
    assert item.scope == text
    assert item.limitations == (text,)


def test_is_immutable_and_slotted():
    item = observation()
    with pytest.raises(FrozenInstanceError):
        item.description = "Changed"
    assert not hasattr(item, "__dict__")


def test_direct_inspection_can_have_no_external_evidence_reference():
    item = observation(
        method=Method.DIRECT_INSPECTION, evidence_ids=(), limitations=(),
    )
    assert item.evidence_ids == ()
    assert item.limitations == ()


def test_evidence_review_requires_references():
    with pytest.raises(ValueError, match="requires evidence"):
        observation(evidence_ids=())


@pytest.mark.parametrize("name", [
    "observation_id", "case_id", "subject_reference", "description", "scope",
])
@pytest.mark.parametrize("value,error", [
    ("", ValueError), ("  ", ValueError), (None, TypeError),
])
def test_rejects_invalid_required_text(name, value, error):
    with pytest.raises(error):
        observation(**{name: value})


@pytest.mark.parametrize("value,error", [
    (True, TypeError), ("1", TypeError),
    (0, ValueError), (-1, ValueError),
])
def test_rejects_invalid_version(value, error):
    with pytest.raises(error):
        observation(observation_version=value)


@pytest.mark.parametrize("name", ["observed_at", "recorded_at"])
@pytest.mark.parametrize("value,error", [
    ("2026-01-01", TypeError),
    (datetime(2026, 1, 1), ValueError),
])
def test_rejects_invalid_temporal_values(name, value, error):
    with pytest.raises(error):
        observation(**{name: value})


def test_rejects_recording_before_observation():
    with pytest.raises(ValueError, match="must not precede"):
        observation(recorded_at=datetime(2025, 1, 1, tzinfo=timezone.utc))


def test_compares_instants_across_offsets_and_preserves_original_offsets():
    instant = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    local = instant.astimezone(timezone(timedelta(hours=-6)))
    item = observation(observed_at=instant, recorded_at=local)
    assert item.observed_at == item.recorded_at
    assert item.recorded_at.isoformat() == "2026-01-01T06:00:00-06:00"


@pytest.mark.parametrize("name,value", [
    ("method", "EVIDENCE_REVIEW"),
    ("declared_observer", "Observer"),
    ("limitations", []),
    ("evidence_ids", []),
    ("limitations", (None,)),
    ("evidence_ids", (1,)),
])
def test_rejects_invalid_types(name, value):
    with pytest.raises(TypeError):
        observation(**{name: value})


@pytest.mark.parametrize("name,value", [
    ("limitations", (" ",)),
    ("evidence_ids", ("",)),
    ("evidence_ids", ("PHOTO-1", "PHOTO-1")),
])
def test_rejects_invalid_collection_content(name, value):
    with pytest.raises(ValueError):
        observation(**{name: value})


def test_references_do_not_require_files_or_create_verification():
    item = observation(evidence_ids=("UNRESOLVED-REFERENCE",))
    assert item.evidence_ids == ("UNRESOLVED-REFERENCE",)
    assert not hasattr(item, "evidence_verified")


def test_new_version_does_not_mutate_original():
    original = observation()
    revised = replace(
        original, observation_version=2, description="Corrected description.",
    )
    assert original.observation_version == 1
    assert revised.observation_version == 2
    assert original.description != revised.description
    assert original.evidence_ids == revised.evidence_ids
