from dataclasses import replace
import unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from sp001.contracts.product001_documentary_commitment import Product001DocumentaryCommitmentKey
from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity
from sp001.contracts.knowledge_source_identity import KnowledgeContentDigest
from sp001.contracts.product001_mvp1_contextual_authorization import (
    ContextualAuthorizationV1, authorization_signing_payload,
    documentary_binding_from_key, verify_contextual_authorization_signature,
)


def key(*, organization="org1", source="source1", version="v1", digest="a" * 64):
    return Product001DocumentaryCommitmentKey(
        organization_id=organization,
        source_identity=KnowledgeSourceIdentity(
            source_id=source, source_version=version,
            source_content_digest=KnowledgeContentDigest(algorithm="SHA-256", value=digest)))


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.key = key()
        unsigned = ContextualAuthorizationV1(
            operation_id="op1", decision_digest="b" * 64, issuer_id="issuer1",
            authority_sequence=1, materialize_deadline=2000000000,
            documentary_binding=documentary_binding_from_key(self.key),
            signature=b"\0" * 64)
        self.cert = replace(unsigned, signature=self.private.sign(authorization_signing_payload(unsigned)))

    def verify(self, cert=None, **kwargs):
        args = dict(trusted_issuer_id="issuer1", trusted_public_key=self.private.public_key(),
                    expected_operation_id="op1", expected_decision_digest="b" * 64,
                    expected_documentary_key=self.key)
        args.update(kwargs)
        return verify_contextual_authorization_signature(cert if cert is not None else self.cert, **args)

    def test_positive_signature_only_not_admission(self):
        self.assertIsNone(self.verify())

    def test_reject_different_document(self):
        with self.assertRaises(PermissionError):
            self.verify(expected_documentary_key=key(source="other"))

    def test_reject_different_version(self):
        with self.assertRaises(PermissionError):
            self.verify(expected_documentary_key=key(version="v2"))

    def test_reject_different_digest(self):
        with self.assertRaises(PermissionError):
            self.verify(expected_documentary_key=key(digest="c" * 64))

    def test_reject_different_operation(self):
        with self.assertRaises(PermissionError):
            self.verify(expected_operation_id="op2")

    def test_reject_altered_signature(self):
        with self.assertRaises(PermissionError):
            self.verify(replace(self.cert, signature=b"\x01" * 64))

    def test_reject_tampered_documentary_binding(self):
        changed = replace(self.cert, documentary_binding=documentary_binding_from_key(key(source="other")))
        with self.assertRaises(PermissionError):
            self.verify(changed, expected_documentary_key=key(source="other"))

    def test_reject_other_organization(self):
        with self.assertRaises(PermissionError):
            self.verify(expected_documentary_key=key(organization="other"))
