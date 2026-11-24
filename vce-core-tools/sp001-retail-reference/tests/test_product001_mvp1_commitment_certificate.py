from dataclasses import replace
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentContextV1,
    verify_commitment_certificate,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)
from sp001.services.product001_mvp1_commitment_issuer import Mvp1CommitmentIssuer
import test_sqlite_product001_mvp1_authorization_store as store_tests


class CommitmentCertificateTests(unittest.TestCase):
    def setUp(self):
        fixture = store_tests.AuthorizationStoreTests()
        self.addCleanup(fixture.doCleanups)
        fixture.setUp()
        self.fixture = fixture
        self.key = Ed25519PrivateKey.generate()
        self.issuer = Mvp1CommitmentIssuer(store=fixture.store, signing_key=self.key)
        self.identity = dict(fixture.identity)
        self.identity["authorization_digest"] = self.identity.pop("expected_digest")
        self.decision = fixture.context["decision_bytes"]
        self.expected = CommitmentContextV1(
            issuer_id="issuer1",
            organization_id=self.identity["organization_id"],
            operation_id="op1",
            authorization_digest=self.identity["authorization_digest"],
            decision_digest=decision_digest_from_canonical_bytes(self.decision),
            materialize_deadline=100,
        )

    def consume(self):
        self.fixture.store.consume(self.fixture.cert, **self.fixture.context)

    def verify(self, certificate, **overrides):
        options = dict(
            trusted_key=self.key.public_key(),
            expected_context=self.expected,
            decision_bytes=self.decision,
            now=99,
        )
        verify_commitment_certificate(certificate, **(options | overrides))

    def test_requires_durable_intent(self):
        self.assertIsNone(self.issuer.issue(**self.identity))
        self.fixture.store.revoke(**self.fixture.identity)
        self.assertIsNone(self.issuer.issue(**self.identity))

    def test_recovery_returns_same_proof_after_revocation(self):
        self.consume()
        original = self.issuer.issue(**self.identity)
        self.verify(original)
        self.fixture.store.revoke(**self.fixture.identity)
        self.assertEqual(self.issuer.issue(**self.identity), original)
        with self.assertRaisesRegex(PermissionError, "deadline expired"):
            self.verify(original, now=100)

    def test_substitution_rejected(self):
        self.consume()
        certificate = self.issuer.issue(**self.identity)
        for field, value in (
            ("issuer_id", "other"),
            ("organization_id", "other"),
            ("operation_id", "other"),
            ("authorization_digest", "0" * 64),
            ("decision_digest", decision_digest_from_canonical_bytes(b"changed")),
            ("materialize_deadline", 101),
        ):
            with self.subTest(field=field):
                changed = replace(certificate.context, **{field: value})
                with self.assertRaisesRegex(PermissionError, "context mismatch"):
                    self.verify(replace(certificate, context=changed))
                decision = b"changed" if field == "decision_digest" else self.decision
                with self.assertRaisesRegex(PermissionError, "invalid commitment signature"):
                    self.verify(
                        replace(certificate, context=changed),
                        expected_context=changed,
                        decision_bytes=decision,
                    )

    def test_other_key_and_other_decision_rejected(self):
        self.consume()
        certificate = self.issuer.issue(**self.identity)
        with self.assertRaisesRegex(PermissionError, "invalid commitment signature"):
            self.verify(certificate, trusted_key=Ed25519PrivateKey.generate().public_key())
        with self.assertRaisesRegex(PermissionError, "context mismatch"):
            self.verify(certificate, decision_bytes=b"changed")
