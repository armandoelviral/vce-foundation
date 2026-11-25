from base64 import b64encode
from dataclasses import asdict

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sp001.contracts.product001_mvp1_commitment_certificate import (
    CommitmentCertificateV1,
    CommitmentContextV1,
    commitment_signing_payload,
    verify_commitment_certificate,
)
from sp001.contracts.product001_mvp1_contextual_authorization import (
    decision_digest_from_canonical_bytes,
)
from sp001.infrastructure.product001_mvp1_http_codec import (
    decode_product001_mvp1_commitment_certificate,
)


@pytest.fixture
def proof():
    decision = b"canonical decision"
    context = CommitmentContextV1(
        issuer_id="issuer",
        organization_id="org",
        operation_id="op",
        authorization_digest="a" * 64,
        decision_digest=decision_digest_from_canonical_bytes(decision),
        materialize_deadline=100,
    )
    signing_key = Ed25519PrivateKey.generate()
    signature = signing_key.sign(commitment_signing_payload(context))
    payload = {
        "version": 1,
        "context": asdict(context),
        "signature_b64": b64encode(signature).decode("ascii"),
    }
    return payload, CommitmentCertificateV1(context, signature), signing_key.public_key(), decision


def test_decoded_certificate_preserves_the_signed_context(proof):
    payload, certificate, key, decision = proof
    decoded = decode_product001_mvp1_commitment_certificate(payload)
    assert decoded == certificate
    verify_commitment_certificate(
        decoded, trusted_key=key, expected_context=certificate.context,
        decision_bytes=decision, now=99,
    )


def test_rejects_legacy_signature_and_request_supplied_key(proof):
    payload, *_ = proof
    with pytest.raises(ValueError):
        decode_product001_mvp1_commitment_certificate(
            {"signature_b64": payload["signature_b64"]},
        )
    with pytest.raises(ValueError):
        decode_product001_mvp1_commitment_certificate(payload | {"public_key": "request key"})


@pytest.mark.parametrize("version", [True, "1", 2])
def test_rejects_unknown_version(proof, version):
    payload, *_ = proof
    with pytest.raises((TypeError, ValueError)):
        decode_product001_mvp1_commitment_certificate(payload | {"version": version})


@pytest.mark.parametrize("changes", [
    {"materialize_deadline": True},
    {"authorization_digest": "a"},
    {"expected_issuer_id": "issuer"},
])
def test_rejects_invalid_context(proof, changes):
    payload, *_ = proof
    with pytest.raises((TypeError, ValueError)):
        decode_product001_mvp1_commitment_certificate(
            payload | {"context": payload["context"] | changes},
        )


def test_rejects_noncanonical_signature_padding_bits(proof):
    payload, *_ = proof
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    canonical = payload["signature_b64"]
    altered = canonical[:-3] + alphabet[alphabet.index(canonical[-3]) + 1] + "=="
    with pytest.raises(ValueError, match="noncanonical"):
        decode_product001_mvp1_commitment_certificate(payload | {"signature_b64": altered})
