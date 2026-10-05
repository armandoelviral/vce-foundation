import inspect

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signature import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing import (
    sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes,
)
from tests.test_security_admission_evidence_coverage_closure_state_merkle_checkpoint_projection import (
    create_checkpoint,
)


def p256_private_key(
    scalar: int = 1,
) -> ec.EllipticCurvePrivateKey:
    return ec.derive_private_key(
        scalar,
        ec.SECP256R1(),
    )


def sign(
    *,
    scalar: int = 1,
    key_id: str = "kms://security-admission/key-001",
):
    checkpoint = create_checkpoint()
    private_key = p256_private_key(scalar)

    signed_checkpoint = (
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=checkpoint,
            key_id=key_id,
            private_key=private_key,
        )
    )

    return checkpoint, private_key, signed_checkpoint


def test_signing_returns_nominal_signature_envelope() -> None:
    checkpoint, _, signed_checkpoint = sign()

    assert isinstance(
        signed_checkpoint,
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSignature,
    )
    assert signed_checkpoint.checkpoint is checkpoint
    assert signed_checkpoint.signature_encoding == "ASN.1-DER"
    assert type(signed_checkpoint.signature) is bytes
    assert signed_checkpoint.signature


def test_signature_verifies_against_exact_canonical_payload() -> None:
    checkpoint, private_key, signed_checkpoint = sign()
    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    private_key.public_key().verify(
        signed_checkpoint.signature,
        payload,
        ec.ECDSA(hashes.SHA256()),
    )


@pytest.mark.parametrize(
    "scalar",
    (
        1,
        2,
        3,
        7,
        19,
        65537,
    ),
)
def test_multiple_p256_keys_produce_verifiable_signatures(
    scalar: int,
) -> None:
    checkpoint, private_key, signed_checkpoint = sign(
        scalar=scalar,
    )
    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    private_key.public_key().verify(
        signed_checkpoint.signature,
        payload,
        ec.ECDSA(hashes.SHA256()),
    )


def test_signature_components_are_positive() -> None:
    _, _, signed_checkpoint = sign()

    r_value, s_value = decode_dss_signature(
        signed_checkpoint.signature
    )

    assert r_value > 0
    assert s_value > 0


def test_signing_key_identity_matches_injected_key() -> None:
    _, private_key, signed_checkpoint = sign(
        scalar=7,
        key_id="hsm://cluster/slot/key-007",
    )

    public_key_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=private_key.public_key(),
        )
    )

    import hashlib

    expected_fingerprint = hashlib.sha256(
        public_key_bytes
    ).hexdigest()

    identity = signed_checkpoint.signing_key_identity

    assert identity.key_id == "hsm://cluster/slot/key-007"
    assert identity.algorithm == "ECDSA-P256-SHA256"
    assert identity.public_key_encoding == "DER-SPKI"
    assert (
        identity.public_key_fingerprint
        == expected_fingerprint
    )


def test_altered_payload_fails_verification() -> None:
    checkpoint, private_key, signed_checkpoint = sign()
    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    with pytest.raises(InvalidSignature):
        private_key.public_key().verify(
            signed_checkpoint.signature,
            payload + b"-altered",
            ec.ECDSA(hashes.SHA256()),
        )


def test_different_checkpoint_fails_verification() -> None:
    _, private_key, signed_checkpoint = sign()
    other_checkpoint = create_checkpoint(
        origin="different-origin",
    )
    other_payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=other_checkpoint,
        )
    )

    with pytest.raises(InvalidSignature):
        private_key.public_key().verify(
            signed_checkpoint.signature,
            other_payload,
            ec.ECDSA(hashes.SHA256()),
        )


def test_different_key_fails_verification() -> None:
    checkpoint, _, signed_checkpoint = sign(
        scalar=1,
    )
    other_public_key = p256_private_key(
        2
    ).public_key()
    payload = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_payload_bytes(
            checkpoint=checkpoint,
        )
    )

    with pytest.raises(InvalidSignature):
        other_public_key.verify(
            signed_checkpoint.signature,
            payload,
            ec.ECDSA(hashes.SHA256()),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        "checkpoint",
        {},
        object(),
    ),
)
def test_signing_requires_nominal_checkpoint(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "checkpoint must be a "
            "SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpoint"
        ),
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=invalid_value,  # type: ignore[arg-type]
            key_id="key-001",
            private_key=p256_private_key(),
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"private-key",
        "private-key",
        object(),
        p256_private_key().public_key(),
    ),
)
def test_signing_requires_private_key(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "private_key must be an "
            "EllipticCurvePrivateKey"
        ),
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=create_checkpoint(),
            key_id="key-001",
            private_key=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "curve",
    (
        ec.SECP384R1(),
        ec.SECP521R1(),
        ec.SECP256K1(),
    ),
)
def test_signing_rejects_other_private_key_curves(
    curve: ec.EllipticCurve,
) -> None:
    private_key = ec.derive_private_key(
        1,
        curve,
    )

    with pytest.raises(
        ValueError,
        match=(
            "private_key curve must be SECP256R1"
        ),
    ):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=create_checkpoint(),
            key_id="key-001",
            private_key=private_key,
        )


@pytest.mark.parametrize(
    "invalid_key_id",
    (
        None,
        1,
        True,
        b"key",
        "",
        " key",
        "key ",
    ),
)
def test_signing_preserves_key_id_validation(
    invalid_key_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint(
            checkpoint=create_checkpoint(),
            key_id=invalid_key_id,  # type: ignore[arg-type]
            private_key=p256_private_key(),
        )


def test_signature_envelope_contains_no_private_key() -> None:
    _, private_key, signed_checkpoint = sign()

    assert not hasattr(signed_checkpoint, "private_key")
    assert not hasattr(
        signed_checkpoint,
        "private_key_bytes",
    )
    assert not hasattr(signed_checkpoint, "credential")
    assert (
        signed_checkpoint.signing_key_identity
        is not private_key
    )


def test_signing_function_does_not_serialize_private_key() -> None:
    source = inspect.getsource(
        sign_security_admission_evidence_coverage_closure_state_merkle_checkpoint
    )

    assert "private_bytes" not in source
    assert "PrivateFormat" not in source
    assert "NoEncryption" not in source


def test_signing_adds_no_decision_or_authority() -> None:
    _, _, signed_checkpoint = sign()

    assert not hasattr(signed_checkpoint, "decision")
    assert not hasattr(signed_checkpoint, "authority")
    assert not hasattr(signed_checkpoint, "authorization")
    assert not hasattr(signed_checkpoint, "admission_status")
