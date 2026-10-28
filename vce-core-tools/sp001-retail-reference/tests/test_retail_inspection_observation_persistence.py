from dataclasses import replace

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
    RetailInspectionObservationIdentity as Identity,
    StoredRetailInspectionObservation as Stored,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_retail_inspection_observations import (
    SqliteRetailInspectionObservationStore as Store,
)
from sp001.services.retail_inspection_observation_persistence import (
    RetailInspectionObservationPersistence as Service,
)


def key(item):
    return Identity(item.observation_id, item.observation_version)


class ReplyStore:
    """Controlled backend responses for boundary validation."""

    def __init__(self, reply):
        self.reply = reply

    def put(self, *, observation):
        return self.reply

    def get(self, *, identity):
        return self.reply


def test_sqlite_roundtrip_retry_and_reopen(tmp_path):
    path = tmp_path / "observations.sqlite3"
    store = Store(database_path=path)
    service = Service(store=store)
    original = observation()
    assert service.save(observation=original) == original
    assert service.save(observation=original) == original
    reopened = Service(store=Store(database_path=path))
    assert reopened.recover(identity=key(original)) == original
    assert store.get(identity=key(original)).document == serialize(original)


def test_conflict_preserves_original_and_new_version(tmp_path):
    service = Service(store=Store(database_path=tmp_path / "observations.sqlite3"))
    original = observation()
    service.save(observation=original)
    changed = replace(original, description="Corrected descriptive content.")
    with pytest.raises(Conflict):
        service.save(observation=changed)
    revised = replace(changed, observation_version=2)
    assert service.save(observation=revised) == revised
    assert service.recover(identity=key(original)) == original
    assert service.recover(identity=key(revised)) == revised


def test_exact_absence(tmp_path):
    service = Service(store=Store(database_path=tmp_path / "observations.sqlite3"))
    assert service.recover(identity=Identity("ABSENT", 1)) is None


@pytest.mark.parametrize("field,value", [
    ("observation_id", "OTHER"),
    ("observation_version", 2),
])
def test_rejects_document_key_mismatch_on_recovery(tmp_path, field, value):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    original = observation()
    changed = replace(original, **{field: value})
    store.put(observation=Stored(key(original), serialize(changed)))
    with pytest.raises(ValueError, match="differs from storage key"):
        Service(store=store).recover(identity=key(original))


def test_rejects_invalid_document_on_recovery(tmp_path):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    identity = Identity("OBS", 1)
    store.put(observation=Stored(identity, "{}"))
    with pytest.raises(ValueError):
        Service(store=store).recover(identity=identity)


def test_rejects_noncanonical_stored_document(tmp_path):
    store = Store(database_path=tmp_path / "observations.sqlite3")
    original = observation()
    store.put(observation=Stored(key(original), serialize(original) + "\n"))
    with pytest.raises(ValueError, match="canonical"):
        Service(store=store).recover(identity=key(original))


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_rejects_wrong_returned_identity(operation):
    original = observation()
    other = replace(original, observation_id="OTHER")
    service = Service(store=ReplyStore(Stored(key(other), serialize(other))))
    with pytest.raises(ValueError, match="different observation identity"):
        if operation == "save":
            service.save(observation=original)
        else:
            service.recover(identity=key(original))


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_rejects_document_mismatch_in_backend_reply(operation):
    original = observation()
    other = replace(original, observation_version=2)
    service = Service(store=ReplyStore(Stored(key(original), serialize(other))))
    with pytest.raises(ValueError, match="differs from storage key"):
        if operation == "save":
            service.save(observation=original)
        else:
            service.recover(identity=key(original))


def test_rejects_changed_content_in_confirmation():
    original = observation()
    changed = replace(original, description="Unexpected replacement.")
    service = Service(store=ReplyStore(Stored(key(original), serialize(changed))))
    with pytest.raises(ValueError, match="confirmation differs"):
        service.save(observation=original)


@pytest.mark.parametrize("reply", [None, "document", object()])
def test_rejects_invalid_confirmation(reply):
    with pytest.raises(TypeError):
        Service(store=ReplyStore(reply)).save(observation=observation())


@pytest.mark.parametrize("reply", ["document", object()])
def test_rejects_invalid_recovered_record(reply):
    with pytest.raises(TypeError):
        Service(store=ReplyStore(reply)).recover(identity=Identity("OBS", 1))


@pytest.mark.parametrize("operation", ["save", "recover"])
def test_backend_errors_propagate(operation):
    failure = OSError("synthetic storage failure")

    class BrokenStore:
        def put(self, *, observation):
            raise failure

        def get(self, *, identity):
            raise failure

    service = Service(store=BrokenStore())
    with pytest.raises(OSError) as caught:
        if operation == "save":
            service.save(observation=observation())
        else:
            service.recover(identity=Identity("OBS", 1))
    assert caught.value is failure


def test_rejects_invalid_dependencies_and_inputs():
    with pytest.raises(TypeError):
        Service(store=object())
    service = Service(store=ReplyStore(None))
    with pytest.raises(TypeError):
        service.save(observation={})
    with pytest.raises(TypeError):
        service.recover(identity="OBS")
