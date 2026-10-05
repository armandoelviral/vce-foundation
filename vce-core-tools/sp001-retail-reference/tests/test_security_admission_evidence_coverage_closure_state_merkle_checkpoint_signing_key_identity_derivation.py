import hashlib
import inspect

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes,
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity,
)


def p256_public_key(
    scalar: int = 1,
) -> ec.EllipticCurvePublicKey:
    return ec.derive_private_key(
        scalar,
        ec.SECP256R1(),
    ).public_key()


def canonical_bytes(
    public_key: ec.EllipticCurvePublicKey,
) -> bytes:
    return (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=public_key,
        )
    )


def derive_identity(
    *,
    key_id: str = "kms://security-admission/key-001",
    public_key: ec.EllipticCurvePublicKey | None = None,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity:
    return (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=key_id,
            public_key=(
                p256_public_key()
                if public_key is None
                else public_key
            ),
        )
    )


def test_canonical_public_key_bytes_match_independent_der_spki() -> None:
    public_key = p256_public_key()

    expected = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    assert canonical_bytes(public_key) == expected


def test_canonical_public_key_bytes_have_exact_bytes_type() -> None:
    assert type(canonical_bytes(p256_public_key())) is bytes


def test_canonical_public_key_bytes_are_deterministic() -> None:
    public_key = p256_public_key()

    first = canonical_bytes(public_key)
    second = canonical_bytes(public_key)
    third = canonical_bytes(public_key)

    assert first == second == third


def test_canonical_public_key_bytes_differ_for_distinct_keys() -> None:
    first = canonical_bytes(p256_public_key(1))
    second = canonical_bytes(p256_public_key(2))

    assert first != second


def test_derived_identity_fields_are_exact() -> None:
    public_key = p256_public_key()
    public_key_bytes = canonical_bytes(public_key)
    expected_fingerprint = hashlib.sha256(
        public_key_bytes
    ).hexdigest()

    identity = derive_identity(
        key_id="kms://security-admission/key-001",
        public_key=public_key,
    )

    assert identity.key_id == (
        "kms://security-admission/key-001"
    )
    assert identity.algorithm == "ECDSA-P256-SHA256"
    assert identity.public_key_encoding == "DER-SPKI"
    assert (
        identity.public_key_fingerprint
        == expected_fingerprint
    )


def test_fingerprint_matches_independent_sha256() -> None:
    public_key = p256_public_key(7)

    expected = hashlib.sha256(
        public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    ).hexdigest()

    assert (
        derive_identity(
            public_key=public_key,
        ).public_key_fingerprint
        == expected
    )


def test_same_public_key_with_different_key_ids_preserves_fingerprint() -> None:
    public_key = p256_public_key()

    first = derive_identity(
        key_id="key-a",
        public_key=public_key,
    )
    second = derive_identity(
        key_id="key-b",
        public_key=public_key,
    )

    assert first.key_id != second.key_id
    assert (
        first.public_key_fingerprint
        == second.public_key_fingerprint
    )


def test_distinct_public_keys_have_distinct_fingerprints() -> None:
    first = derive_identity(
        public_key=p256_public_key(1),
    )
    second = derive_identity(
        public_key=p256_public_key(2),
    )

    assert (
        first.public_key_fingerprint
        != second.public_key_fingerprint
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
def test_multiple_p256_public_keys_are_supported(
    scalar: int,
) -> None:
    public_key = p256_public_key(scalar)
    identity = derive_identity(
        public_key=public_key,
    )

    assert len(identity.public_key_fingerprint) == 64
    assert identity.algorithm == "ECDSA-P256-SHA256"


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"public-key",
        "public-key",
        object(),
        ec.derive_private_key(1, ec.SECP256R1()),
    ),
)
def test_canonical_bytes_require_public_key(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "public_key must be an "
            "EllipticCurvePublicKey"
        ),
    ):
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "curve",
    (
        ec.SECP384R1(),
        ec.SECP521R1(),
        ec.SECP256K1(),
    ),
)
def test_other_elliptic_curves_are_rejected(
    curve: ec.EllipticCurve,
) -> None:
    public_key = ec.derive_private_key(
        1,
        curve,
    ).public_key()

    with pytest.raises(
        ValueError,
        match=(
            "public_key curve must be SECP256R1"
        ),
    ):
        canonical_bytes(public_key)


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
def test_derivation_preserves_identity_key_id_validation(
    invalid_key_id: object,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=invalid_key_id,  # type: ignore[arg-type]
            public_key=p256_public_key(),
        )


def test_derivation_does_not_export_private_key_bytes() -> None:
    source = inspect.getsource(
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity
    )
    canonical_source = inspect.getsource(
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes
    )

    assert "PrivateFormat" not in source
    assert "private_bytes" not in source
    assert "PrivateFormat" not in canonical_source
    assert "private_bytes" not in canonical_source


def test_identity_contains_only_public_key_fingerprint() -> None:
    identity = derive_identity()

    assert not hasattr(identity, "public_key")
    assert not hasattr(identity, "private_key")
    assert not hasattr(identity, "private_key_bytes")
    assert not hasattr(identity, "credential")


def test_derivation_does_not_sign_or_verify() -> None:
    source = inspect.getsource(
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity
    )

    assert ".sign(" not in source
    assert ".verify(" not in source
