from dataclasses import replace
import sqlite3

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from test_sqlite_case_access_issuance_preparations import setup
from sp001.contracts.case_access_grant_administration import (
    GrantAdministrationAction as Action,
)
from sp001.infrastructure.prepared_case_access_credentials import (
    PreparedCaseAccessSigner, PreparedCredentialProtector,
)
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    SqliteCaseAccessIssuanceCompletions, PreparedCaseAccessCompleter,
)
from sp001.services.case_access_issuance_reference_validation import (
    IssuanceReferenceValidationError,
)


@pytest.fixture
def components(tmp_path):
    path, _, binding, command, preparation = setup(tmp_path)
    store = SqliteCaseAccessIssuanceCompletions(database_path=path)
    store.prepare(preparation=preparation, at_time=150)
    signer = PreparedCaseAccessSigner(
        signing_key_id="KEY-1",
        private_key=rsa.generate_private_key(public_exponent=65537, key_size=2048),
        issuer="access", audience="coordinator",
    )
    protector = PreparedCredentialProtector(
        protection_key_id="PROTECTION-1", key=b"x" * 32,
    )
    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector, clock=lambda: 150,
    )
    return path, store, binding, command, preparation, signer, protector, completer


def test_delivery_follows_durable_completion_and_reopen(components):
    path, store, _, _, preparation, signer, protector, completer = components
    token = completer.complete(request_id=preparation.request_id)
    reopened = SqliteCaseAccessIssuanceCompletions(database_path=path)
    completed = reopened.read_completed(request_id=preparation.request_id)
    assert completed.completed_at == 150
    assert protector.recover(
        preparation=preparation, protected=completed.protected,
    ) == token
    assert token.credential not in repr(completed)
    with sqlite3.connect(path) as connection:
        row = connection.execute(
            "SELECT status, ciphertext FROM case_access_issuance_completions"
        ).fetchone()
    assert row[0] == "COMPLETED"
    assert token.credential.encode() not in row[1]
    replay = PreparedCaseAccessCompleter(
        store=reopened, signer=signer, protector=protector, clock=lambda: 150,
    )
    assert replay.complete(request_id=preparation.request_id) == token
    assert reopened.read_completed(request_id=preparation.request_id) == completed


@pytest.mark.parametrize("mutation", ["revoke", "binding", "expire"])
def test_change_during_signing_prevents_completion(components, monkeypatch, mutation):
    path, store, binding, command, preparation, signer, protector, completer = components
    original = signer.sign
    now = [150]

    def sign_then_change(**kwargs):
        token = original(**kwargs)
        writer = SqliteCaseAccessIssuanceCompletions(database_path=path)
        if mutation == "revoke":
            writer.apply(record=replace(
                command, event_id="REVOKE-1", action=Action.REVOKE,
            ))
        elif mutation == "binding":
            writer.put_binding(
                snapshot=replace(binding, binding=replace(binding.binding, revision=2)),
                expected_revision=1,
            )
        else:
            now[0] = preparation.payload.expires_at
        return token

    monkeypatch.setattr(signer, "sign", sign_then_change)
    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=protector, clock=lambda: now[0],
    )
    with pytest.raises(IssuanceReferenceValidationError):
        completer.complete(request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is None


def test_failed_persistence_does_not_recover_or_deliver(components, monkeypatch):
    path, store, _, _, preparation, _, protector, completer = components
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER fail_completion BEFORE INSERT
            ON case_access_issuance_completions
            BEGIN SELECT RAISE(ABORT, 'injected completion failure'); END
        """)
    recovered = []

    def forbidden_recover(**kwargs):
        recovered.append(True)
        raise AssertionError("recovery must follow commit")

    monkeypatch.setattr(protector, "recover", forbidden_recover)
    with pytest.raises(sqlite3.IntegrityError):
        completer.complete(request_id=preparation.request_id)
    assert recovered == []
    assert store.read_completed(request_id=preparation.request_id) is None
    assert store.read_prepared(request_id=preparation.request_id) == preparation


def test_revoked_completion_cannot_be_delivered_again(components):
    _, store, _, command, preparation, _, _, completer = components
    completer.complete(request_id=preparation.request_id)
    historical = store.read_completed(request_id=preparation.request_id)
    store.apply(record=replace(
        command, event_id="REVOKE-AFTER", action=Action.REVOKE,
    ))
    with pytest.raises(IssuanceReferenceValidationError):
        completer.complete(request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) == historical
