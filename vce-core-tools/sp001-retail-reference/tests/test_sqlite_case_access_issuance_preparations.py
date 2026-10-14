from dataclasses import replace
import sqlite3

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.case_access_context import CaseAccessPermission, CaseAccessOperation
from sp001.contracts.case_access_grant import CaseAccessGrant
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationRecord, GrantAdministrationAction as Action,
)
from sp001.contracts.case_access_issuance_preparation import (
    FederatedPrincipalBinding, CaseAccessTokenPayload,
    IssuanceGrantReference, CaseAccessIssuancePreparation,
)
from sp001.contracts.federated_principal_binding_snapshot import FederatedPrincipalBindingSnapshot
from sp001.infrastructure.sqlite_case_access_issuance_preparations import (
    SqliteCaseAccessIssuancePreparations,
)
from sp001.services.case_access_issuance_reference_validation import IssuanceReferenceValidationError


def setup(tmp_path):
    path = tmp_path / "authorization.sqlite3"
    store = SqliteCaseAccessIssuancePreparations(database_path=path)
    permission = CaseAccessPermission("CASE-001", CaseAccessOperation.READ_STATE)
    binding = FederatedPrincipalBinding(
        "BINDING-1", 1, AuthenticatedPrincipal("external", "external-subject"), "internal",
    )
    snapshot = FederatedPrincipalBindingSnapshot(binding, True)
    assert store.put_binding(snapshot=snapshot, expected_revision=None)
    grant = CaseAccessGrant(
        "GRANT-1", AuthenticatedPrincipal("access", "internal"), permission, 90, 250,
    )
    command = GrantAdministrationRecord(
        "CREATE-1", AuthenticatedPrincipal("access", "admin"), Action.GRANT, grant, 90,
    )
    store.apply(record=command)
    preparation = CaseAccessIssuancePreparation(
        "REQUEST-1", binding,
        CaseAccessTokenPayload("access", "internal", "coordinator", 100, 100, 200,
                               "TOKEN-1", (permission,)),
        "KEY-1", (IssuanceGrantReference("GRANT-1", 1, permission, 250),),
    )
    return path, store, snapshot, command, preparation


def test_prepared_survives_reopen_and_exact_replay(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    assert store.prepare(preparation=preparation, at_time=150) == preparation
    reopened = SqliteCaseAccessIssuancePreparations(database_path=path)
    assert reopened.read_prepared(request_id="REQUEST-1") == preparation
    reopened.prepare(preparation=preparation, at_time=150)
    with sqlite3.connect(path) as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM case_access_issuance_preparations"
        ).fetchone()[0] == 1


@pytest.mark.parametrize("kind", ["binding_revision", "binding_inactive", "revoked_grant"])
def test_changed_references_prevent_preparation(tmp_path, kind):
    path, store, binding, command, preparation = setup(tmp_path)
    writer = SqliteCaseAccessIssuancePreparations(database_path=path)
    if kind == "revoked_grant":
        writer.apply(record=replace(command, event_id="REVOKE-1", action=Action.REVOKE))
    else:
        updated = replace(binding, binding=replace(binding.binding, revision=2),
                          active=kind != "binding_inactive")
        assert writer.put_binding(snapshot=updated, expected_revision=1)
    with pytest.raises(IssuanceReferenceValidationError):
        store.prepare(preparation=preparation, at_time=150)
    assert store.read_prepared(request_id="REQUEST-1") is None


def test_conflicting_request_id_does_not_replace_preparation(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    store.prepare(preparation=preparation, at_time=150)
    changed = replace(preparation, signing_key_id="OTHER-KEY")
    with pytest.raises(ValueError, match="request_id conflicts"):
        store.prepare(preparation=changed, at_time=150)
    assert store.read_prepared(request_id="REQUEST-1") == preparation


def test_replay_after_revocation_cannot_readmit(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    store.prepare(preparation=preparation, at_time=150)
    store.apply(record=replace(command, event_id="REVOKE-1", action=Action.REVOKE))
    with pytest.raises(IssuanceReferenceValidationError):
        store.prepare(preparation=preparation, at_time=150)
    assert store.read_prepared(request_id="REQUEST-1") == preparation


def test_binding_current_and_history_roll_back_together(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER fail_binding_history BEFORE INSERT ON federated_binding_history
            BEGIN SELECT RAISE(ABORT, 'injected history failure'); END
        """)
    updated = replace(binding, binding=replace(binding.binding, revision=2), active=False)
    with pytest.raises(sqlite3.IntegrityError):
        store.put_binding(snapshot=updated, expected_revision=1)
    assert store.prepare(preparation=preparation, at_time=150) == preparation


def test_stale_binding_update_is_rejected(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    updated = replace(binding, binding=replace(binding.binding, revision=2))
    assert store.put_binding(snapshot=updated, expected_revision=1)
    conflicting = replace(updated, active=False)
    assert not store.put_binding(snapshot=conflicting, expected_revision=1)


def test_duplicate_token_id_rolls_back_new_preparation(tmp_path):
    path, store, binding, command, preparation = setup(tmp_path)
    store.prepare(preparation=preparation, at_time=150)
    with pytest.raises(sqlite3.IntegrityError):
        store.prepare(
            preparation=replace(preparation, request_id="REQUEST-2"), at_time=150,
        )
    assert store.read_prepared(request_id="REQUEST-2") is None
