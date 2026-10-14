from dataclasses import replace
import sqlite3
import threading

import pytest

from test_sqlite_case_access_issuance_preparations import setup
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
)
from sp001.infrastructure import sqlite_case_access_issuance_preparations as module
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


@pytest.mark.parametrize("mutation", ["revoke_grant", "deactivate_binding"])
def test_other_writer_cannot_interleave_validation_and_prepared_insert(
    tmp_path, monkeypatch, mutation,
):
    path, store, binding, command, preparation = setup(tmp_path)
    validation_finished = threading.Event()
    lock_attempt_finished = threading.Event()
    writer_outcomes = []
    writer_errors = []
    original_validator = module.validate_issuance_references

    def competing_writer():
        try:
            if not validation_finished.wait(timeout=5):
                raise AssertionError("preparation did not reach validation barrier")
            connection = sqlite3.connect(path, timeout=0)
            try:
                try:
                    connection.execute("BEGIN IMMEDIATE")
                except sqlite3.OperationalError as error:
                    assert error.sqlite_errorcode == sqlite3.SQLITE_BUSY
                    writer_outcomes.append("blocked")
                else:
                    connection.rollback()
                    writer_outcomes.append("unexpected_write_lock")
            finally:
                connection.close()
        except BaseException as error:
            writer_errors.append(error)
        finally:
            lock_attempt_finished.set()

    def validate_then_pause(**kwargs):
        original_validator(**kwargs)
        validation_finished.set()
        if not lock_attempt_finished.wait(timeout=5):
            raise AssertionError("competing writer did not finish its lock attempt")
        assert writer_errors == []
        assert writer_outcomes == ["blocked"]

    monkeypatch.setattr(module, "validate_issuance_references", validate_then_pause)
    thread = threading.Thread(target=competing_writer, daemon=True)
    thread.start()
    try:
        assert store.prepare(preparation=preparation, at_time=150) == preparation
    finally:
        validation_finished.set()
        thread.join(timeout=5)
    assert not thread.is_alive()
    assert writer_errors == []
    assert writer_outcomes == ["blocked"]

    # After PREPARED commits, another adapter can perform the real mutation.
    monkeypatch.setattr(module, "validate_issuance_references", original_validator)
    writer = module.SqliteCaseAccessIssuancePreparations(database_path=path)
    if mutation == "revoke_grant":
        assert writer.apply(record=replace(
            command, event_id="REVOKE-CONCURRENT",
            action=Action.REVOKE, recorded_at=150,
        ))
        assert writer.read_grant_snapshot(grant_id="GRANT-1").revoked
    else:
        assert writer.put_binding(
            snapshot=replace(
                binding, binding=replace(binding.binding, revision=2), active=False,
            ),
            expected_revision=1,
        )

    # Historical evidence remains, but current references prevent readmission.
    assert writer.read_prepared(request_id="REQUEST-1") == preparation
    with pytest.raises(IssuanceReferenceValidationError):
        store.prepare(preparation=preparation, at_time=150)


def test_revocation_committed_before_preparation_prevents_insert(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    errors = []

    def revoke():
        try:
            writer = module.SqliteCaseAccessIssuancePreparations(database_path=path)
            assert writer.apply(record=replace(
                command, event_id="REVOKE-FIRST", action=Action.REVOKE,
                recorded_at=150,
            ))
        except BaseException as error:
            errors.append(error)

    thread = threading.Thread(target=revoke, daemon=True)
    thread.start()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert errors == []
    with pytest.raises(IssuanceReferenceValidationError):
        store.prepare(preparation=preparation, at_time=150)
    assert store.read_prepared(request_id="REQUEST-1") is None
