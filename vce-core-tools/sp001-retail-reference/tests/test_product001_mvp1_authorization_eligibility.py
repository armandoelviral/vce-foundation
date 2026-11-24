from dataclasses import replace
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest, KnowledgeSourceIdentity
from sp001.contracts.product001_documentary_commitment import Product001DocumentaryCommitmentKey
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1, authorization_signing_payload, documentary_binding_from_key,
)
from sp001.contracts.product001_mvp1_authorization_eligibility import (
    AuthoritativeAuthorizationSnapshotV1, EligibilityStatus, authorization_digest,
    evaluate_authorization_eligibility, snapshot_signing_payload,
)


class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.auth_key = Ed25519PrivateKey.generate()
        self.snapshot_key = Ed25519PrivateKey.generate()
        self.document = Product001DocumentaryCommitmentKey(
            organization_id="org1", source_identity=KnowledgeSourceIdentity(
                source_id="doc1", source_version="v1",
                source_content_digest=KnowledgeContentDigest(algorithm="SHA-256", value="a" * 64)))
        unsigned = ContextualAuthorizationV1(
            operation_id="op1", decision_digest="b" * 64, issuer_id="issuer1",
            authority_sequence=3, materialize_deadline=200,
            documentary_binding=documentary_binding_from_key(self.document), signature=b"\0" * 64)
        self.cert = replace(unsigned, signature=self.auth_key.sign(authorization_signing_payload(unsigned)))
        self.snapshot = self.make_snapshot()

    def make_snapshot(self, **changes):
        values = dict(issuer_id="issuer1", operation_id="op1",
                      authorization_digest=authorization_digest(self.cert), revision=10,
                      authority_sequence=3, revoked=False, consumed=False,
                      observed_at=100, signature=b"\0" * 64)
        values.update(changes)
        unsigned = AuthoritativeAuthorizationSnapshotV1(**values)
        return replace(unsigned, signature=self.snapshot_key.sign(snapshot_signing_payload(unsigned)))

    def evaluate(self, cert=None, snapshot="default", **changes):
        args = dict(trusted_issuer_id="issuer1",
                    trusted_authorization_key=self.auth_key.public_key(),
                    trusted_snapshot_key=self.snapshot_key.public_key(),
                    expected_operation_id="op1", expected_decision_digest="b" * 64,
                    expected_documentary_key=self.document, now=105, max_snapshot_age=10)
        args.update(changes)
        return evaluate_authorization_eligibility(
            self.cert if cert is None else cert,
            self.snapshot if snapshot == "default" else snapshot, **args)

    def test_snapshot_relative_positive_not_admission(self):
        result = self.evaluate()
        self.assertEqual(result.status, EligibilityStatus.ELIGIBLE)
        self.assertEqual(result.reason, "SNAPSHOT_RELATIVE_ONLY")

    def test_revoked(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(revoked=True)).status, EligibilityStatus.REJECTED)

    def test_superseded_sequence(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(authority_sequence=4)).status, EligibilityStatus.REJECTED)

    def test_sequence_behind_indeterminate(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(authority_sequence=2)).status, EligibilityStatus.INDETERMINATE)

    def test_deadline_not_renewed(self):
        self.assertEqual(self.evaluate(now=200, snapshot=self.make_snapshot(observed_at=200)).reason, "DEADLINE_EXPIRED")

    def test_consumed(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(consumed=True)).status, EligibilityStatus.REJECTED)

    def test_operation_mismatch(self):
        self.assertEqual(self.evaluate(expected_operation_id="other").status, EligibilityStatus.REJECTED)

    def test_snapshot_missing(self):
        self.assertEqual(self.evaluate(snapshot=None).status, EligibilityStatus.INDETERMINATE)

    def test_snapshot_stale(self):
        self.assertEqual(self.evaluate(now=111).status, EligibilityStatus.INDETERMINATE)

    def test_snapshot_future(self):
        self.assertEqual(self.evaluate(now=99).status, EligibilityStatus.INDETERMINATE)

    def test_snapshot_signature_tampered(self):
        self.assertEqual(self.evaluate(snapshot=replace(self.snapshot, signature=b"\1" * 64)).status, EligibilityStatus.INDETERMINATE)

    def test_snapshot_wrong_certificate(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(authorization_digest="c" * 64)).status, EligibilityStatus.INDETERMINATE)

    def test_snapshot_wrong_operation(self):
        self.assertEqual(self.evaluate(snapshot=self.make_snapshot(operation_id="other")).status, EligibilityStatus.INDETERMINATE)

    def test_certificate_signature_tampered(self):
        self.assertEqual(self.evaluate(cert=replace(self.cert, signature=b"\1" * 64)).status, EligibilityStatus.REJECTED)

    def test_untrusted_snapshot_key(self):
        self.assertEqual(self.evaluate(trusted_snapshot_key=Ed25519PrivateKey.generate().public_key()).status, EligibilityStatus.INDETERMINATE)


if __name__ == "__main__":
    unittest.main()
