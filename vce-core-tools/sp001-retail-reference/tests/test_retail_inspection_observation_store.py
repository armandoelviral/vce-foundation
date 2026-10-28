from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
    RetailInspectionObservationIdentity as Identity,
    RetailInspectionObservationStore as Store,
    StoredRetailInspectionObservation as Stored,
)


def record(observation_id="OBS", version=1, document="opaque document"):
    return Stored(Identity(observation_id, version), document)


class ReferenceStore:
    """Sequential illustrative double; no durability or concurrency guarantee."""

    def __init__(self):
        self.records = {}

    def put(self, *, observation):
        existing = self.records.get(observation.identity)
        if existing is not None:
            if existing.document != observation.document:
                raise Conflict("identity/version conflict")
            return existing
        self.records[observation.identity] = observation
        return observation

    def get(self, *, identity):
        return self.records.get(identity)


def test_preserves_exact_identity_and_document():
    identity = Identity(" OBS ", 2)
    text = "  exact document\n"
    item = Stored(identity, text)
    assert item.identity is identity
    assert item.document == text


@pytest.mark.parametrize("value,error", [
    ("", ValueError), (" ", ValueError),
    (None, TypeError), (1, TypeError), (True, TypeError),
])
def test_rejects_invalid_observation_id(value, error):
    with pytest.raises(error):
        Identity(value, 1)


@pytest.mark.parametrize("value,error", [
    (0, ValueError), (-1, ValueError),
    (True, TypeError), ("1", TypeError), (None, TypeError),
])
def test_rejects_invalid_version(value, error):
    with pytest.raises(error):
        Identity("OBS", value)


@pytest.mark.parametrize("value,error", [
    ("", ValueError), (" ", ValueError),
    (None, TypeError), (b"bytes", TypeError), (1, TypeError),
])
def test_rejects_invalid_document(value, error):
    with pytest.raises(error):
        record(document=value)


def test_rejects_non_nominal_identity():
    with pytest.raises(TypeError):
        Stored(("OBS", 1), "document")


def test_values_are_frozen_and_slotted():
    item = record()
    with pytest.raises(FrozenInstanceError):
        item.document = "replacement"
    with pytest.raises(FrozenInstanceError):
        item.identity.observation_version = 2
    assert not hasattr(item, "__dict__")
    assert not hasattr(item.identity, "__dict__")


def test_reference_double_illustrates_identical_retry():
    store = ReferenceStore()
    assert isinstance(store, Store)
    first = record()
    assert store.put(observation=first) is first
    assert store.put(observation=replace(first)) is first
    assert len(store.records) == 1


def test_reference_double_illustrates_conflict_without_replacement():
    store = ReferenceStore()
    original = record()
    store.put(observation=original)
    with pytest.raises(Conflict):
        store.put(observation=replace(original, document="different"))
    assert store.get(identity=original.identity) is original
    assert len(store.records) == 1


def test_reference_double_preserves_original_and_corrected_versions():
    store = ReferenceStore()
    original = record()
    corrected = record(version=2, document="corrected description")
    store.put(observation=original)
    store.put(observation=corrected)
    assert store.get(identity=original.identity) is original
    assert store.get(identity=corrected.identity) is corrected
    assert len(store.records) == 2


def test_reference_double_separates_observations_with_same_version():
    store = ReferenceStore()
    first = record("OBS-A")
    second = record("OBS-B")
    store.put(observation=first)
    store.put(observation=second)
    assert store.get(identity=first.identity) is first
    assert store.get(identity=second.identity) is second


def test_reference_double_does_not_require_consecutive_versions():
    store = ReferenceStore()
    later = record(version=7)
    earlier = record(version=2)
    store.put(observation=later)
    store.put(observation=earlier)
    assert store.get(identity=later.identity) is later
    assert store.get(identity=earlier.identity) is earlier
    assert store.get(identity=Identity("OBS", 1)) is None


def test_reference_double_returns_none_for_exact_absence():
    store = ReferenceStore()
    store.put(observation=record())
    assert store.get(identity=Identity("OBS", 2)) is None
    assert store.get(identity=Identity("OTHER", 1)) is None
