import ast
import inspect
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.services import (
    security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity
    as identity_module,
)
from sp001.services.security_admission_evidence_coverage_closure_state_merkle_checkpoint_signing_key_identity import (
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING,
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_FINGERPRINT_ALGORITHM,
    SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM,
    SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity,
)


def create_identity(
    *,
    key_id: str = "kms://security-admission/key-001",
    fingerprint: str = "a" * 64,
) -> SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity:
    return (
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id=key_id,
            algorithm="ECDSA-P256-SHA256",
            public_key_encoding="DER-SPKI",
            public_key_fingerprint=fingerprint,
        )
    )


def test_identity_fields_are_exact() -> None:
    identity_fields = fields(
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
    )

    assert tuple(field.name for field in identity_fields) == (
        "key_id",
        "algorithm",
        "public_key_encoding",
        "public_key_fingerprint",
    )
    assert tuple(field.type for field in identity_fields) == (
        str,
        str,
        str,
        str,
    )


def test_identity_is_immutable_and_slotted() -> None:
    identity = create_identity()

    assert not hasattr(identity, "__dict__")

    with pytest.raises(FrozenInstanceError):
        identity.key_id = "changed"  # type: ignore[misc]


def test_cryptographic_profile_constants_are_exact() -> None:
    assert (
        SECURITY_ADMISSION_MERKLE_CHECKPOINT_SIGNATURE_ALGORITHM
        == "ECDSA-P256-SHA256"
    )
    assert (
        SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_ENCODING
        == "DER-SPKI"
    )
    assert (
        SECURITY_ADMISSION_MERKLE_CHECKPOINT_PUBLIC_KEY_FINGERPRINT_ALGORITHM
        == "SHA-256"
    )


def test_exact_values_are_preserved() -> None:
    identity = create_identity(
        key_id="arn:aws:kms:region:account:key/key-001",
        fingerprint="1" * 64,
    )

    assert identity.key_id == (
        "arn:aws:kms:region:account:key/key-001"
    )
    assert identity.algorithm == "ECDSA-P256-SHA256"
    assert identity.public_key_encoding == "DER-SPKI"
    assert identity.public_key_fingerprint == "1" * 64


@pytest.mark.parametrize(
    "key_id",
    (
        "kms://security-admission/key-001",
        "arn:aws:kms:region:account:key/key-001",
        "gcp-kms://project/location/key-ring/key/version/1",
        "azure-key-vault://vault/key/version",
        "hsm://cluster/slot/key-001",
    ),
)
def test_nonempty_key_identifiers_are_preserved(
    key_id: str,
) -> None:
    identity = create_identity(key_id=key_id)

    assert identity.key_id == key_id


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"key",
        object(),
    ),
)
def test_key_id_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="key_id must be a str",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id=invalid_value,  # type: ignore[arg-type]
            algorithm="ECDSA-P256-SHA256",
            public_key_encoding="DER-SPKI",
            public_key_fingerprint="a" * 64,
        )


def test_key_id_rejects_empty_string() -> None:
    with pytest.raises(
        ValueError,
        match="key_id must not be empty",
    ):
        create_identity(key_id="")


@pytest.mark.parametrize(
    "invalid_value",
    (
        " ",
        "\t",
        "\n",
        " key",
        "key ",
        "\tkey",
        "key\n",
    ),
)
def test_key_id_rejects_surrounding_whitespace(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "key_id must not contain surrounding whitespace"
        ),
    ):
        create_identity(key_id=invalid_value)


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"ECDSA-P256-SHA256",
        object(),
    ),
)
def test_algorithm_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="algorithm must be a str",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id="key-001",
            algorithm=invalid_value,  # type: ignore[arg-type]
            public_key_encoding="DER-SPKI",
            public_key_fingerprint="a" * 64,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "ECDSA",
        "ECDSA-P384-SHA384",
        "ED25519",
        "ML-DSA-65",
        "ecdsa-p256-sha256",
    ),
)
def test_algorithm_rejects_other_profiles(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "algorithm must be ECDSA-P256-SHA256"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id="key-001",
            algorithm=invalid_value,
            public_key_encoding="DER-SPKI",
            public_key_fingerprint="a" * 64,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"DER-SPKI",
        object(),
    ),
)
def test_public_key_encoding_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="public_key_encoding must be a str",
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id="key-001",
            algorithm="ECDSA-P256-SHA256",
            public_key_encoding=invalid_value,  # type: ignore[arg-type]
            public_key_fingerprint="a" * 64,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "PEM",
        "DER",
        "RAW",
        "der-spki",
    ),
)
def test_public_key_encoding_rejects_other_profiles(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "public_key_encoding must be DER-SPKI"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id="key-001",
            algorithm="ECDSA-P256-SHA256",
            public_key_encoding=invalid_value,
            public_key_fingerprint="a" * 64,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        1,
        True,
        b"a" * 64,
        object(),
    ),
)
def test_fingerprint_requires_exact_string(
    invalid_value: object,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "public_key_fingerprint must be a str"
        ),
    ):
        SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity(
            key_id="key-001",
            algorithm="ECDSA-P256-SHA256",
            public_key_encoding="DER-SPKI",
            public_key_fingerprint=invalid_value,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        "",
        "a" * 63,
        "a" * 65,
        "A" * 64,
        "g" * 64,
        "0x" + ("a" * 64),
        "a" * 32,
    ),
)
def test_fingerprint_requires_canonical_sha256_hex(
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "public_key_fingerprint must contain "
            "64 lowercase hexadecimal characters"
        ),
    ):
        create_identity(fingerprint=invalid_value)


@pytest.mark.parametrize(
    "fingerprint",
    (
        "0" * 64,
        "1" * 64,
        "a" * 64,
        "f" * 64,
        "0123456789abcdef" * 4,
    ),
)
def test_canonical_fingerprints_are_preserved(
    fingerprint: str,
) -> None:
    identity = create_identity(
        fingerprint=fingerprint,
    )

    assert identity.public_key_fingerprint == fingerprint


def test_identity_contains_no_private_key_material() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
        )
    }

    assert "private_key" not in field_names
    assert "private_key_bytes" not in field_names
    assert "secret" not in field_names
    assert "credential" not in field_names


def test_identity_does_not_execute_cryptography() -> None:
    source = inspect.getsource(identity_module)
    tree = ast.parse(source)

    imported_names = {
        alias.name
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    function_names = {
        node.name
        for node in tree.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    assert "cryptography" not in imported_names
    assert "hashlib" not in imported_names
    assert "sign" not in function_names
    assert "verify" not in function_names


def test_identity_grants_no_authority() -> None:
    field_names = {
        field.name
        for field in fields(
            SecurityAdmissionEvidenceCoverageClosureStateMerkleCheckpointSigningKeyIdentity
        )
    }

    assert "authority" not in field_names
    assert "authorization" not in field_names
    assert "decision" not in field_names
    assert "admission_status" not in field_names
