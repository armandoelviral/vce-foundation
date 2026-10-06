import inspect
from dataclasses import FrozenInstanceError, fields, replace

import pytest
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity_derivation import (
    canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes,
    derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_binding import (
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding,
)


KEY_ID = "kms://security-admission/key-001"


def p256_public_key(
    scalar: int = 1,
) -> ec.EllipticCurvePublicKey:
    return ec.derive_private_key(
        scalar,
        ec.SECP256R1(),
    ).public_key()


def create_binding(
    *,
    scalar: int = 1,
    key_id: str = KEY_ID,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding:
    public_key = p256_public_key(scalar)
    identity = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=key_id,
            public_key=public_key,
        )
    )
    public_key_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=public_key,
        )
    )

    return SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
        signing_key_identity=identity,
        public_key_bytes=public_key_bytes,
    )


def test_binding_has_exact_fields() -> None:
    assert tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
        )
    ) == (
        "signing_key_identity",
        "public_key_bytes",
    )


def test_binding_preserves_exact_values() -> None:
    public_key = p256_public_key()
    identity = (
        derive_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity(
            key_id=KEY_ID,
            public_key=public_key,
        )
    )
    public_key_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=public_key,
        )
    )

    binding = SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
        signing_key_identity=identity,
        public_key_bytes=public_key_bytes,
    )

    assert binding.signing_key_identity is identity
    assert binding.public_key_bytes is public_key_bytes


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
def test_multiple_p256_public_keys_bind(
    scalar: int,
) -> None:
    binding = create_binding(
        scalar=scalar,
    )

    assert (
        binding.signing_key_identity.public_key_fingerprint
    )
    assert binding.public_key_bytes


@pytest.mark.parametrize(
    "key_id",
    (
        "kms://security-admission/key-001",
        "hsm://cluster/slot/key-007",
        "gcp-kms://project/location/key/version",
        "azure-key-vault://vault/key/version",
    ),
)
def test_opaque_key_identifiers_are_preserved(
    key_id: str,
) -> None:
    binding = create_binding(
        key_id=key_id,
    )

    assert binding.signing_key_identity.key_id == key_id


def test_binding_is_frozen() -> None:
    binding = create_binding()

    with pytest.raises(FrozenInstanceError):
        binding.public_key_bytes = b"changed"


def test_binding_uses_slots() -> None:
    binding = create_binding()

    assert not hasattr(binding, "__dict__")


def test_equal_values_are_equal() -> None:
    assert create_binding() == create_binding()


def test_different_public_keys_are_not_equal() -> None:
    assert create_binding(scalar=1) != create_binding(
        scalar=2
    )


@pytest.mark.parametrize(
    "value",
    (
        None,
        object(),
        "identity",
        b"identity",
        1,
        True,
        (),
    ),
)
def test_signing_key_identity_rejects_invalid_type(
    value: object,
) -> None:
    public_key = p256_public_key()
    public_key_bytes = (
        canonical_security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_public_key_bytes(
            public_key=public_key,
        )
    )

    with pytest.raises(
        TypeError,
        match="signing_key_identity",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=value,
            public_key_bytes=public_key_bytes,
        )


@pytest.mark.parametrize(
    "value",
    (
        None,
        bytearray(b"key"),
        memoryview(b"key"),
        "key",
        1,
        True,
        (),
        object(),
    ),
)
def test_public_key_bytes_reject_invalid_type(
    value: object,
) -> None:
    identity = create_binding().signing_key_identity

    with pytest.raises(
        TypeError,
        match="public_key_bytes",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=identity,
            public_key_bytes=value,
        )


def test_public_key_bytes_reject_empty_value() -> None:
    identity = create_binding().signing_key_identity

    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=identity,
            public_key_bytes=b"",
        )


@pytest.mark.parametrize(
    "value",
    (
        b"not-der",
        b"\x30\x00",
        b"\x00" * 91,
    ),
)
def test_public_key_bytes_reject_malformed_der(
    value: bytes,
) -> None:
    identity = create_binding().signing_key_identity

    with pytest.raises(
        ValueError,
        match="DER-SPKI",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=identity,
            public_key_bytes=value,
        )


def test_public_key_bytes_reject_non_ec_key() -> None:
    public_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    ).public_key()
    public_key_bytes = public_key.public_bytes(
        Encoding.DER,
        PublicFormat.SubjectPublicKeyInfo,
    )
    identity = create_binding().signing_key_identity

    with pytest.raises(
        ValueError,
        match="elliptic-curve",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=identity,
            public_key_bytes=public_key_bytes,
        )


def test_public_key_bytes_reject_wrong_curve() -> None:
    public_key = ec.derive_private_key(
        1,
        ec.SECP384R1(),
    ).public_key()
    public_key_bytes = public_key.public_bytes(
        Encoding.DER,
        PublicFormat.SubjectPublicKeyInfo,
    )
    identity = create_binding().signing_key_identity

    with pytest.raises(
        ValueError,
        match="SECP256R1",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=identity,
            public_key_bytes=public_key_bytes,
        )


def test_identity_rejects_different_public_key() -> None:
    first = create_binding(
        scalar=1,
    )
    second = create_binding(
        scalar=2,
    )

    with pytest.raises(
        ValueError,
        match="must match",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=first.signing_key_identity,
            public_key_bytes=second.public_key_bytes,
        )


def test_fingerprint_mutation_is_rejected() -> None:
    binding = create_binding()
    fingerprint = (
        binding
        .signing_key_identity
        .public_key_fingerprint
    )
    replacement = (
        "0" if fingerprint[0] != "0" else "1"
    )
    changed_identity = replace(
        binding.signing_key_identity,
        public_key_fingerprint=(
            replacement + fingerprint[1:]
        ),
    )

    with pytest.raises(
        ValueError,
        match="must match",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding(
            signing_key_identity=changed_identity,
            public_key_bytes=binding.public_key_bytes,
        )


def test_binding_contains_no_private_key() -> None:
    field_names = tuple(
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
        )
    )
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
    )

    assert "private_key" not in field_names
    assert "private_bytes" not in source


def test_binding_does_not_claim_trust_or_authority() -> None:
    source = inspect.getsource(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningPublicKeyBinding
    )
    forbidden = (
        "trusted",
        "authority",
        "authorization",
        "admission_decision",
        "rejection",
    )

    assert all(
        token not in source.lower()
        for token in forbidden
    )
