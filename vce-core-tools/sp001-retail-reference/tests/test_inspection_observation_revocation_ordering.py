from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest

import test_sqlite_authorized_inspection_observations as setup
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
    GrantAdministrationRecord,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)
from sp001.infrastructure.sqlite_retail_inspection_observations import (
    SqliteRetailInspectionObservationStore as Store,
)


class ObservedConnection:
    """Observe transaction entry and hold either form of explicit commit."""

    def __init__(
        self, connection, *, began=None, before_commit=None, release=None,
    ):
        self.connection = connection
        self.began = began
        self.before_commit = before_commit
        self.release = release

    def _before_commit(self):
        if self.before_commit is not None:
            assert self.connection.in_transaction
            self.before_commit.set()
            if not self.release.wait(timeout=10):
                raise TimeoutError("test did not release transaction")

    def execute(self, sql, *args, **kwargs):
        command = sql.strip().upper()
        if command.startswith("BEGIN") and self.began is not None:
            self.began.set()
        if command == "COMMIT":
            self._before_commit()
        return self.connection.execute(sql, *args, **kwargs)

    def commit(self):
        self._before_commit()
        return self.connection.commit()

    def __getattr__(self, name):
        return getattr(self.connection, name)


def instrument(monkeypatch, owner, **events):
    if isinstance(owner, setup.SqliteCaseAccessGrants):
        original = owner._connection

        @contextmanager
        def connection_context():
            with original() as connection:
                yield ObservedConnection(connection, **events)

        monkeypatch.setattr(owner, "_connection", connection_context)
    else:
        original = owner._connect

        def connect():
            return ObservedConnection(original(), **events)

        monkeypatch.setattr(owner, "_connect", connect)


def revoke(grants, principal, definition):
    return grants.apply(record=GrantAdministrationRecord(
        f"REVOKE-{definition.grant_id}", principal,
        Action.REVOKE, definition, 150,
    ))


def test_revocation_commits_first_denies_waiting_save(tmp_path, monkeypatch):
    path, _, backend, principal, grants = setup.environment(tmp_path)
    definition = setup.grant(grants, principal, setup.SAVE)
    context = setup.access(principal, setup.SAVE)
    item = setup.observation()

    held = Event()
    release = Event()
    save_began = Event()
    instrument(
        monkeypatch, grants, before_commit=held, release=release,
    )
    instrument(monkeypatch, backend, began=save_began)

    with ThreadPoolExecutor(max_workers=2) as executor:
        revocation = executor.submit(revoke, grants, principal, definition)
        try:
            assert held.wait(timeout=5), "revocation did not reach COMMIT"
            saving = executor.submit(
                backend.save_authorized, access=context, observation=item,
            )
            assert save_began.wait(timeout=5), "save did not attempt BEGIN"
        finally:
            release.set()

        revocation.result(timeout=10)
        with pytest.raises(setup.Denied):
            saving.result(timeout=10)

    store = Store(database_path=path)
    assert store.get(identity=setup.key(item)) is None
    assert setup.count(path) == 0
    assert grants.permits(
        principal=principal, permission=definition.permission, at_time=150,
    ) is False


def test_save_commits_first_preserves_record_and_denies_retry(
    tmp_path, monkeypatch,
):
    path, _, backend, principal, grants = setup.environment(tmp_path)
    definition = setup.grant(grants, principal, setup.SAVE)
    context = setup.access(principal, setup.SAVE)
    item = setup.observation()

    held = Event()
    release = Event()
    revoke_began = Event()
    instrument(
        monkeypatch, backend, before_commit=held, release=release,
    )
    instrument(monkeypatch, grants, began=revoke_began)

    with ThreadPoolExecutor(max_workers=2) as executor:
        saving = executor.submit(
            backend.save_authorized, access=context, observation=item,
        )
        try:
            assert held.wait(timeout=5), "save did not reach COMMIT"
            revocation = executor.submit(revoke, grants, principal, definition)
            assert revoke_began.wait(timeout=5), "revocation did not attempt BEGIN"
        finally:
            release.set()

        assert saving.result(timeout=10) == item
        revocation.result(timeout=10)

    assert grants.permits(
        principal=principal, permission=definition.permission, at_time=150,
    ) is False
    with pytest.raises(setup.Denied):
        backend.save_authorized(access=context, observation=item)

    reopened = Store(database_path=path)
    stored = reopened.get(identity=setup.key(item))
    assert stored is not None
    assert stored.document == serialize(item)
    assert setup.count(path) == 1
