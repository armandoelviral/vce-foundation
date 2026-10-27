import json
import sqlite3
from dataclasses import replace

from sp001.contracts.case_access_issuance_preparation import (
    FederatedPrincipalBinding,
)
from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.federated_principal_binding_snapshot import (
    FederatedPrincipalBindingSnapshot,
)
from sp001.infrastructure.sqlite_case_access_issuance_preparations import (
    SqliteCaseAccessIssuancePreparations,
)


def make_snapshot(binding_id, subject, internal_subject):
    return FederatedPrincipalBindingSnapshot(
        binding=FederatedPrincipalBinding(
            binding_id=binding_id,
            revision=1,
            external_principal=AuthenticatedPrincipal("ISSUER", subject),
            internal_subject=internal_subject,
        ),
        active=True,
    )


def read_documents(path, table):
    # Los nombres de tabla son constantes definidas por esta prueba.
    assert table in {
        "federated_principal_bindings",
        "federated_binding_history",
    }

    with sqlite3.connect(path) as connection:
        rows = connection.execute(
            f"SELECT document FROM {table} ORDER BY binding_id, revision"
        ).fetchall()

    return tuple(json.loads(row[0]) for row in rows)


def test_distinct_external_principals_can_share_internal_subject(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteCaseAccessIssuancePreparations(database_path=path)

    first = make_snapshot("BINDING-1", "ACCOUNT-1", "PERSON-1")
    second = make_snapshot("BINDING-2", "ACCOUNT-2", "PERSON-1")

    assert store.put_binding(snapshot=first, expected_revision=None)
    assert store.put_binding(snapshot=second, expected_revision=None)

    current = read_documents(path, "federated_principal_bindings")
    history = read_documents(path, "federated_binding_history")

    assert len(current) == 2
    assert len(history) == 2
    assert {
        item["binding"]["external_principal"]["subject"]
        for item in current
    } == {"ACCOUNT-1", "ACCOUNT-2"}
    assert {
        item["binding"]["internal_subject"]
        for item in current
    } == {"PERSON-1"}


def test_later_revision_can_change_internal_subject_and_preserves_history(tmp_path):
    path = tmp_path / "bindings.sqlite3"
    store = SqliteCaseAccessIssuancePreparations(database_path=path)

    original = make_snapshot("BINDING-1", "ACCOUNT-1", "PERSON-1")
    assert store.put_binding(snapshot=original, expected_revision=None)

    updated = replace(
        original,
        binding=replace(
            original.binding,
            revision=2,
            internal_subject="PERSON-2",
        ),
    )
    assert store.put_binding(snapshot=updated, expected_revision=1)

    current = read_documents(path, "federated_principal_bindings")
    history = read_documents(path, "federated_binding_history")

    assert len(current) == 1
    assert current[0]["binding"]["revision"] == 2
    assert current[0]["binding"]["internal_subject"] == "PERSON-2"

    assert [
        (item["binding"]["revision"], item["binding"]["internal_subject"])
        for item in history
    ] == [(1, "PERSON-1"), (2, "PERSON-2")]
