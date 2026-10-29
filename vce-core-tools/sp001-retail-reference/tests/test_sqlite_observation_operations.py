import sqlite3
from dataclasses import replace

import pytest

import test_sqlite_authorized_inspection_observations as setup
from sp001.contracts.retail_observation_operation import (
    RetailObservationSaveRequest as Request,
    RetailObservationEffectDisposition as Disposition,
    RetailObservationOperationConflict,
)
from sp001.infrastructure.sqlite_observation_operations import (
    SqliteObservationOperations as Backend,
)


def environment(tmp_path):
    path, now, _, principal, grants = setup.environment(tmp_path)
    backend = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: now[0],
    )
    setup.grant(grants, principal, setup.SAVE)
    return path, backend, setup.access(principal, setup.SAVE)


def counts(path):
    with sqlite3.connect(path) as connection:
        return tuple(connection.execute(
            "SELECT COUNT(*) FROM " + table
        ).fetchone()[0] for table in (
            "retail_inspection_observations", "retail_observation_operations",
        ))


def test_created_retry_and_reopen_preserve_original_receipt(tmp_path):
    path, backend, access = environment(tmp_path)
    request = Request("REQUEST", setup.observation())
    first = backend.save_operation_authorized(access=access, request=request)
    assert first.disposition is Disposition.CREATED

    reopened = Backend(
        database_path=path, expected_audience="OBS", clock=lambda: 150,
    )
    assert reopened.save_operation_authorized(
        access=access, request=request,
    ) == first
    assert counts(path) == (1, 1)


def test_preexisting_observation_is_reused_not_attributed_as_created(tmp_path):
    path, backend, access = environment(tmp_path)
    item = setup.observation()
    backend.save_authorized(access=access, observation=item)
    assert counts(path) == (1, 0)
    receipt = backend.save_operation_authorized(
        access=access, request=Request("REQUEST", item),
    )
    assert receipt.disposition is Disposition.REUSED
    assert counts(path) == (1, 1)


def test_new_request_for_identical_content_has_distinct_reused_receipt(tmp_path):
    path, backend, access = environment(tmp_path)
    item = setup.observation()
    first = backend.save_operation_authorized(
        access=access, request=Request("FIRST", item),
    )
    second = backend.save_operation_authorized(
        access=access, request=Request("SECOND", item),
    )
    assert first.disposition is Disposition.CREATED
    assert second.disposition is Disposition.REUSED
    assert counts(path) == (1, 2)


def test_same_operation_different_intent_conflicts_without_replacement(tmp_path):
    path, backend, access = environment(tmp_path)
    request = Request("REQUEST", setup.observation())
    original = backend.save_operation_authorized(access=access, request=request)
    changed = replace(request, observation=replace(
        request.observation, description="Different description.",
    ))
    with pytest.raises(RetailObservationOperationConflict):
        backend.save_operation_authorized(access=access, request=changed)
    assert backend.save_operation_authorized(
        access=access, request=request,
    ) == original
    assert counts(path) == (1, 1)


def test_observation_conflict_creates_no_new_receipt(tmp_path):
    path, backend, access = environment(tmp_path)
    item = setup.observation()
    backend.save_operation_authorized(
        access=access, request=Request("FIRST", item),
    )
    with pytest.raises(setup.Conflict):
        backend.save_operation_authorized(
            access=access,
            request=Request("SECOND", replace(item, description="Different.")),
        )
    assert counts(path) == (1, 1)


def test_receipt_insert_failure_rolls_back_new_effect(tmp_path):
    path, backend, access = environment(tmp_path)
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER reject_receipt BEFORE INSERT
            ON retail_observation_operations
            BEGIN SELECT RAISE(ABORT, 'synthetic receipt failure'); END
        """)
    with pytest.raises(sqlite3.IntegrityError):
        backend.save_operation_authorized(
            access=access, request=Request("REQUEST", setup.observation()),
        )
    assert counts(path) == (0, 0)


def test_missing_grant_prevents_effect_and_receipt(tmp_path):
    path, backend, _ = environment(tmp_path)
    other = setup.AuthenticatedPrincipal("ISSUER", "OTHER")
    with pytest.raises(setup.Denied):
        backend.save_operation_authorized(
            access=setup.access(other, setup.SAVE),
            request=Request("REQUEST", setup.observation()),
        )
    assert counts(path) == (0, 0)


def test_profile_is_verified_on_operation_connection(tmp_path):
    path, backend, access = environment(tmp_path)
    original = backend._connect

    def downgraded():
        connection = original()
        connection.execute("PRAGMA synchronous=NORMAL")
        return connection

    backend._connect = downgraded
    with pytest.raises(RuntimeError, match="WAL"):
        backend.save_operation_authorized(
            access=access, request=Request("REQUEST", setup.observation()),
        )
    assert counts(path) == (0, 0)
