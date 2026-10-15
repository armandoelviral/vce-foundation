import sqlite3

import pytest

from test_case_access_issuance_completion import components
from sp001.contracts.prepared_case_access_crypto import (
    PreparedAccessTokenSigner, PreparedAccessCredentialProtector,
)
from sp001.contracts.protected_case_access_credential import (
    ProtectedCaseAccessCredential,
)
from sp001.infrastructure.sqlite_case_access_issuance_completions import (
    PreparedCaseAccessCompleter,
)


def test_distinct_adapters_preserve_transaction_boundaries_and_replay(components):
    path, store, _, _, preparation, signer, protector, _ = components
    events = []

    def prove_write_lock_is_available():
        with sqlite3.connect(path, timeout=0) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.rollback()

    class Signer:
        def sign(self, *, preparation):
            prove_write_lock_is_available()
            events.append("sign")
            return signer.sign(preparation=preparation)

    class Protector:
        def protect(self, *, preparation, token):
            prove_write_lock_is_available()
            events.append("protect")
            return protector.protect(preparation=preparation, token=token)

        def recover(self, *, preparation, protected):
            # Another connection must observe the committed completion.
            with sqlite3.connect(path) as connection:
                row = connection.execute(
                    "SELECT status FROM case_access_issuance_completions "
                    "WHERE request_id=?", (preparation.request_id,),
                ).fetchone()
            assert row == ("COMPLETED",)
            events.append("recover")
            return protector.recover(
                preparation=preparation, protected=protected,
            )

    alternate_signer = Signer()
    alternate_protector = Protector()
    assert isinstance(alternate_signer, PreparedAccessTokenSigner)
    assert isinstance(alternate_protector, PreparedAccessCredentialProtector)
    completer = PreparedCaseAccessCompleter(
        store=store, signer=alternate_signer, protector=alternate_protector,
        clock=lambda: 150,
    )
    token = completer.complete(request_id=preparation.request_id)
    assert events == ["sign", "protect", "recover"]
    assert completer.complete(request_id=preparation.request_id) == token
    assert events == ["sign", "protect", "recover", "recover"]


def test_invalid_signer_result_cannot_be_persisted(components):
    _, store, _, _, preparation, _, protector, _ = components

    class Signer:
        def sign(self, *, preparation):
            return "untyped-credential"

    completer = PreparedCaseAccessCompleter(
        store=store, signer=Signer(), protector=protector, clock=lambda: 150,
    )
    with pytest.raises(TypeError, match="signer"):
        completer.complete(request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is None


def test_invalid_protection_result_cannot_be_persisted(components):
    _, store, _, _, preparation, signer, _, _ = components

    class Protector:
        def protect(self, *, preparation, token):
            return object()

        def recover(self, *, preparation, protected):
            pytest.fail("must not recover without confirmation")

    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=Protector(), clock=lambda: 150,
    )
    with pytest.raises(TypeError, match="protector"):
        completer.complete(request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is None


def test_recovery_result_is_checked_after_commit(components):
    _, store, _, _, preparation, signer, protector, _ = components

    class Protector:
        def protect(self, *, preparation, token):
            return protector.protect(preparation=preparation, token=token)

        def recover(self, *, preparation, protected):
            return "untyped-credential"

    completer = PreparedCaseAccessCompleter(
        store=store, signer=signer, protector=Protector(), clock=lambda: 150,
    )
    with pytest.raises(TypeError, match="protector"):
        completer.complete(request_id=preparation.request_id)
    assert store.read_completed(request_id=preparation.request_id) is not None


def test_envelope_import_preserves_nominal_identity():
    from sp001.infrastructure.prepared_case_access_credentials import (
        ProtectedCaseAccessCredential as CompatibilityImport,
    )
    assert CompatibilityImport is ProtectedCaseAccessCredential
