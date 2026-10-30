import sqlite3
from dataclasses import replace

import pytest

import test_sqlite_authorized_inspection_observations as setup
from test_sqlite_observation_operations import environment
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationOperationIdentity as Identity,
    RetailObservationEffectDisposition as Disposition,
    RetailObservationOperationConflict,
)
from sp001.infrastructure.sqlite_observation_operations import (
    SqliteObservationOperations as Backend,
)


class ConfirmationLost(OSError):
    """Synthetic response loss after the real SQLite COMMIT succeeds."""


class LosingConnection:
    def __init__(self, connection, owner):
        self.connection = connection
        self.owner = owner

    def execute(self, sql, *args, **kwargs):
        result = self.connection.execute(sql, *args, **kwargs)
        if sql.strip().upper() == "COMMIT" and self.owner.armed:
            self.owner.armed = False
            assert not self.connection.in_transaction
            self.owner.committed = True
            raise ConfirmationLost("synthetic commit response loss")
        return result

    def __getattr__(self, name):
        return getattr(self.connection, name)


class LosingBackend(Backend):
    def __init__(self, **kwargs):
        self.armed = False
        self.committed = False
        super().__init__(**kwargs)

    def _connect(self):
        return LosingConnection(super()._connect(), self)


def rows(path):
    with sqlite3.connect(path) as connection:
        effects = connection.execute("""
            SELECT observation_id, observation_version, document
            FROM retail_inspection_observations
            ORDER BY observation_id, observation_version
        """).fetchall()
        receipts = connection.execute("""
            SELECT issuer, subject, case_id, request_id,
                   observation_id, observation_version, document, disposition
            FROM retail_observation_operations
            ORDER BY issuer, subject, case_id, request_id
        """).fetchall()
    return effects, receipts


def commit_with_lost_response(tmp_path, *, reused=False):
    path, backend, access = environment(tmp_path)
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    setup.grant(grants, access.principal, setup.READ)
    request = Request("REQUEST", setup.observation())
    if reused:
        backend.save_authorized(
            access=access, observation=request.observation,
        )
    losing = LosingBackend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    losing.armed = True
    with pytest.raises(ConfirmationLost):
        losing.save_operation_authorized(access=access, request=request)
    assert losing.committed
    identity = Identity(
        access.principal, request.observation.case_id, request.request_id,
    )
    return path, access, request, identity


@pytest.mark.parametrize("reused", [False, True])
def test_reopen_and_retry_preserve_exact_committed_pair(tmp_path, reused):
    path, access, request, identity = commit_with_lost_response(
        tmp_path, reused=reused,
    )
    before = rows(path)
    assert tuple(map(len, before)) == (1, 1)
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    recovered = reopened.recover_operation_authorized(
        access=setup.access(access.principal, setup.READ),
        identity=identity,
    )
    assert recovered is not None
    assert recovered.disposition is (
        Disposition.REUSED if reused else Disposition.CREATED
    )
    assert recovered.operation == identity

    for _ in range(2):
        assert reopened.save_operation_authorized(
            access=access, request=request,
        ) == recovered
    assert rows(path) == before


def test_contradictory_retry_preserves_original_pair(tmp_path):
    path, access, request, identity = commit_with_lost_response(tmp_path)
    before = rows(path)
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    changed = replace(request, observation=replace(
        request.observation, description="Contradictory replacement.",
    ))
    with pytest.raises(RetailObservationOperationConflict):
        reopened.save_operation_authorized(access=access, request=changed)
    assert rows(path) == before
    recovered = reopened.recover_operation_authorized(
        access=setup.access(access.principal, setup.READ), identity=identity,
    )
    assert recovered.stored_observation.document == setup.serialize(
        request.observation,
    )


def test_revocation_blocks_recovery_and_retry_after_confirmed_commit(tmp_path):
    path, access, request, identity = commit_with_lost_response(tmp_path)
    before = rows(path)
    grants = setup.SqliteCaseAccessGrants(database_path=path)
    for operation in (setup.SAVE, setup.READ):
        definition = setup.grant(grants, access.principal, operation)
        assert grants.apply(record=setup.GrantAdministrationRecord(
            "REVOKE-" + operation.value,
            access.principal, setup.Action.REVOKE, definition, 150,
        ))
    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    with pytest.raises(setup.Denied):
        reopened.recover_operation_authorized(
            access=setup.access(access.principal, setup.READ),
            identity=identity,
        )
    with pytest.raises(setup.Denied):
        reopened.save_operation_authorized(access=access, request=request)
    assert rows(path) == before
