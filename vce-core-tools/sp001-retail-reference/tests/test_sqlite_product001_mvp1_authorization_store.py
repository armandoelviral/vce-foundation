from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sp001.contracts.product001_mvp1_authorization_eligibility import authorization_digest
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1,
    authorization_signing_payload,
    decision_digest_from_canonical_bytes,
    documentary_binding_from_key,
)
from sp001.infrastructure.sqlite_product001_mvp1_authorization_store import (
    AuthorizationConflict,
    SqliteMvp1AuthorizationStore,
)
from test_product001_mvp1_contextual_authorization import key


class AuthorizationStoreTests(unittest.TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        private = Ed25519PrivateKey.generate()
        document = key()
        decision = b'{"decision":"approve"}'
        unsigned = ContextualAuthorizationV1(
            operation_id="op1",
            issuer_id="issuer1",
            decision_digest=decision_digest_from_canonical_bytes(decision),
            authority_sequence=1,
            materialize_deadline=100,
            documentary_binding=documentary_binding_from_key(document),
            signature=bytes(64),
        )
        self.cert = replace(
            unsigned, signature=private.sign(authorization_signing_payload(unsigned)),
        )
        self.context = dict(operation_id="op1", decision_bytes=decision, documentary_key=document)
        self.identity = dict(
            organization_id=document.organization_id,
            operation_id="op1",
            expected_digest=authorization_digest(self.cert),
        )
        self.now = 99
        self.config = dict(
            database_path=Path(folder) / "authority.sqlite3",
            issuer_id="issuer1",
            public_key=private.public_key(),
            clock=lambda: self.now,
        )
        self.store = SqliteMvp1AuthorizationStore(**self.config)
        self.assertTrue(self.store.register(self.cert, **self.context))

    def test_revocation_first_denies_and_registration_does_not_reopen(self):
        self.assertTrue(self.store.revoke(**self.identity))
        self.assertFalse(self.store.register(self.cert, **self.context))
        with self.assertRaisesRegex(PermissionError, "revoked"):
            self.store.consume(self.cert, **self.context)
        self.assertIsNone(self.store.recover(**self.identity))

    def test_consumption_first_recovers_original_after_revocation_and_expiry(self):
        original = self.store.consume(self.cert, **self.context)
        self.assertTrue(self.store.revoke(**self.identity))
        self.now = 101
        self.assertEqual(original.materialize_deadline, 100)
        self.assertEqual(original.decision_bytes, self.context["decision_bytes"])
        self.assertEqual(self.store.recover(**self.identity), original)
        with self.assertRaises(PermissionError):
            self.store.consume(self.cert, **self.context)

    def test_concurrent_consumers_create_one_intent(self):
        barrier = Barrier(2)

        def consume():
            barrier.wait(timeout=5)
            try:
                return self.store.consume(self.cert, **self.context)
            except PermissionError as error:
                self.assertEqual(str(error), "authorization already consumed")
                return None

        with ThreadPoolExecutor(max_workers=2) as pool:
            attempts = [pool.submit(consume) for _ in range(2)]
            results = [attempt.result(timeout=10) for attempt in attempts]
        winners = [intent for intent in results if intent is not None]
        self.assertEqual(len(winners), 1)
        self.assertEqual(self.store.recover(**self.identity), winners[0])

    def test_failure_after_insert_rolls_back_consumption_and_intent(self):
        class FailingStore(SqliteMvp1AuthorizationStore):
            @contextmanager
            def _write(self):
                with super()._write() as connection:
                    yield connection
                    raise RuntimeError("before commit")

        failing = FailingStore(**self.config)
        with self.assertRaisesRegex(RuntimeError, "before commit"):
            failing.consume(self.cert, **self.context)
        self.assertIsNone(self.store.recover(**self.identity))
        self.store.consume(self.cert, **self.context)
        self.assertIsNotNone(self.store.recover(**self.identity))

    def test_lost_response_is_reconciled_by_reading_after_reopen(self):
        def lose_response():
            self.store.consume(self.cert, **self.context)
            raise ConnectionError("commit response lost")

        with self.assertRaises(ConnectionError):
            lose_response()
        reopened = SqliteMvp1AuthorizationStore(**self.config)
        intent = reopened.recover(**self.identity)
        self.assertEqual(intent.authorization_digest, self.identity["expected_digest"])
        self.assertEqual(intent.materialize_deadline, 100)
        with self.assertRaises(AuthorizationConflict):
            reopened.recover(**(self.identity | {"expected_digest": "0" * 64}))
        with self.assertRaisesRegex(PermissionError, "already consumed"):
            reopened.consume(self.cert, **self.context)

    def test_exact_context_and_exclusive_deadline(self):
        with self.assertRaisesRegex(PermissionError, "context mismatch"):
            self.store.consume(self.cert, **(self.context | {"decision_bytes": b"other"}))
        self.now = 100
        with self.assertRaisesRegex(PermissionError, "deadline expired"):
            self.store.consume(self.cert, **self.context)
        self.assertIsNone(self.store.recover(**self.identity))
