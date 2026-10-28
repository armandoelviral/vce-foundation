import sqlite3
from dataclasses import replace

import pytest

from test_retail_inspection_observation import observation
from sp001.contracts.retail_inspection_observation_store import (
    RetailInspectionObservationConflict as Conflict,
    RetailInspectionObservationIdentity as Identity,
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


class ConfirmationLost(OSError):
    """Synthetic failure after a successful SQLite commit."""


class CommitResponseLossConnection:
    """Delegate to a real connection, then lose one COMMIT response."""

    def __init__(self, connection, owner):
        self.connection = connection
        self.owner = owner

    def execute(self, sql, parameters=()):
        result = self.connection.execute(sql, parameters)
        if sql.strip().upper() == "COMMIT" and self.owner.armed:
            self.owner.armed = False
            assert not self.connection.in_transaction
            self.owner.committed = True
            raise ConfirmationLost("synthetic commit response loss")
        return result

    @property
    def in_transaction(self):
        return self.connection.in_transaction

    def close(self):
        self.connection.close()


class LosingStore(Store):
    """Instrument the connection; retain the production put algorithm."""

    def __init__(self, **kwargs):
        self.armed = False
        self.committed = False
        super().__init__(**kwargs)
        self.armed = True

    def _connect(self):
        return CommitResponseLossConnection(super()._connect(), self)


def key(item):
    return Identity(item.observation_id, item.observation_version)


def rows(path):
    with sqlite3.connect(path) as connection:
        return connection.execute("""
            SELECT observation_id, observation_version, document
            FROM retail_inspection_observations
            ORDER BY observation_id, observation_version
        """).fetchall()


def commit_with_lost_response(path):
    store = LosingStore(database_path=path)
    original = observation()
    with pytest.raises(ConfirmationLost):
        Service(store=store).save(observation=original)
    assert store.committed
    return original


def test_reopen_recovers_committed_observation_after_response_loss(tmp_path):
    path = tmp_path / "observations.sqlite3"
    original = commit_with_lost_response(path)

    service = Service(store=Store(database_path=path))
    assert service.recover(identity=key(original)) == original
    assert rows(path) == [(
        original.observation_id,
        str(original.observation_version),
        serialize(original),
    )]


def test_retry_preserves_one_exact_record(tmp_path):
    path = tmp_path / "observations.sqlite3"
    original = commit_with_lost_response(path)
    before = rows(path)

    service = Service(store=Store(database_path=path))
    assert service.save(observation=original) == original
    assert service.save(observation=original) == original
    assert rows(path) == before
    assert len(before) == 1


def test_contradictory_retry_cannot_replace_committed_content(tmp_path):
    path = tmp_path / "observations.sqlite3"
    original = commit_with_lost_response(path)
    before = rows(path)

    service = Service(store=Store(database_path=path))
    changed = replace(original, description="Contradictory replacement.")
    with pytest.raises(Conflict):
        service.save(observation=changed)

    assert rows(path) == before
    assert service.recover(identity=key(original)) == original


def test_correction_uses_new_version_and_preserves_original(tmp_path):
    path = tmp_path / "observations.sqlite3"
    original = commit_with_lost_response(path)
    service = Service(store=Store(database_path=path))
    corrected = replace(
        original,
        observation_version=2,
        description="A separately recorded correction.",
    )

    assert service.save(observation=corrected) == corrected
    reopened = Service(store=Store(database_path=path))
    assert reopened.recover(identity=key(original)) == original
    assert reopened.recover(identity=key(corrected)) == corrected
    assert rows(path) == [
        (original.observation_id, "1", serialize(original)),
        (corrected.observation_id, "2", serialize(corrected)),
    ]
